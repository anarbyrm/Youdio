from typing import Any, Dict, List

from django.conf import settings
from googleapiclient.discovery import build
from urllib.parse import urljoin
from requests.sessions import Session

from core.constants import SERVICE_NAME, VERSION, YOUTUBE_API_BASE_URL, RequestType
from core.utils.helpers import get_video_url_from_youtube_page, get_youtube_audio_stream_url


class YouTubeService:
    def __init__(self):
        self.order_by_statistics = False

    def send_request(self, url: str, data: dict = None, params: dict = None, method="GET") -> Any:
        response = Session().request(
            url=url,
            method=method,
            params=params,
            json=data,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise response.raise_for_status()

    def initiate_list_request(self, request_type: RequestType, **kwargs) -> Any:
        youtube = build(SERVICE_NAME, VERSION, developerKey=settings.YOUTUBE_API_KEY)

        if request_type == RequestType.SEARCH:
            request = youtube.search()
        elif request_type == RequestType.PLAYLISTS:
            request = youtube.playlists()
        elif request_type == RequestType.PLAYLIST_ITEMS:
            request = youtube.playlistItems()
        return request.list(**kwargs)

    def get_channels_data(self, username: str) -> str:
        searcher = self.initiate_list_request(
            RequestType.SEARCH,
            part="snippet",
            type="channel",
            maxResults=10,
            q=username,
        )
        channels_data = searcher.execute()
        prepared_channels = self.prepare_data(channels_data["items"])
        return prepared_channels

    def get_playlists_by_channel_id(self, channel_id: str) -> List[Dict[str, Any]]:
        result = []

        prev_page_token = None
        total = None
        count = 0
        limit = 50

        while True:
            try:
                if total and count >= total:
                    break

                pagination = {}

                if prev_page_token:
                    pagination["pageToken"] = prev_page_token

                searcher = self.initiate_list_request(
                    RequestType.PLAYLISTS,
                    part="snippet,status,contentDetails,id",
                    channelId=channel_id,
                    maxResults=limit,
                    **pagination
                )

                playlists = searcher.execute()
                prev_page_token = playlists["nextPageToken"] if "nextPageToken" in playlists else None

                if not total:
                    total = playlists["pageInfo"]["totalResults"]

                prepared_playlists = self.prepare_data(playlists["items"])
                result.extend(prepared_playlists)
                count += limit

            except Exception as exp:
                return None

        return result

    def prepare_data(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        This function modifies data to be ready for serialization.
        """
        result = []

        for data in data_list:
            snippet = data.pop("snippet")
            thumbnail = snippet.pop("thumbnails", {}).get("high")
            status = data.pop("status", None)
            content_count_data = data.pop("contentDetails", None)
            statistics = data.pop("statistics", None)
            player = data.pop("player", None)

            # dictionary modification
            data.update(snippet)
            data["thumbnail_url"] = thumbnail["url"]

            if status:
                data["status"] = status["privacyStatus"]

            if content_count_data:
                item_count = content_count_data.get("itemCount")
                if item_count:
                    data["item_count"] = item_count

                video_id = content_count_data.get("videoId")
                if video_id:
                    data["video_id"] = video_id

            if statistics:
                data.update({
                    "view_count": statistics.get("viewCount"),
                    "like_count": statistics.get("likeCount"),
                    "comment_count": statistics.get("commentCount")
                })

            if player:
                video_url = get_video_url_from_youtube_page(player["embedHtml"])
                data["audio_stream_url"] = get_youtube_audio_stream_url(video_url)

            result.append(data)

        return result

    def get_playlist_videos(self, playlist_id: str) -> List[Dict[str, Any]]:
        searcher = self.initiate_list_request(
            RequestType.PLAYLIST_ITEMS,
            part="snippet,contentDetails",
            maxResults=50,
            playlistId=playlist_id
        )
        playlist_items = searcher.execute()
        prepared_playlist_items = self.prepare_data(playlist_items["items"])
        return prepared_playlist_items

    def get_video_detail(self, video_id: str) -> List[Dict[str, Any]]:
        url = urljoin(YOUTUBE_API_BASE_URL, "videos")
        params = {
            "key": settings.YOUTUBE_API_KEY,
            "part": "statistics,snippet,player",
            "id": video_id,
            "maxResults": 1,
        }
        response = self.send_request(url, params=params)
        if response:
            prepared_video_detail = self.prepare_data(response["items"])
            return prepared_video_detail
