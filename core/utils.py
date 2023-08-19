from typing import Any, Dict, List

from django.conf import settings
from googleapiclient.discovery import build
from urllib.parse import urljoin
from requests.sessions import Session

from .constants import SERVICE_NAME, VERSION, YOUTUBE_API_BASE_URL, RequestType


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

    def initiate_list_request(self, request_type: RequestType, **kwargs) -> Any:
        youtube = build(SERVICE_NAME, VERSION, developerKey=settings.YOUTUBE_API_KEY)

        if request_type == RequestType.SEARCH:
            request = youtube.search()
        elif request_type == RequestType.PLAYLISTS:
            request = youtube.playlists()
        return request.list(**kwargs)

    def get_channels_data(self, username: str) -> str:
        try:
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
        except Exception as exp:
            return None

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
                    part="snippet,status,contentDetails",
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
            thumbnails = snippet.pop("thumbnails")
            default_thumbnail = thumbnails.get("default")
            status = data.pop("status", None)
            content_count_data = data.pop("contentDetails", None)

            # dictionary modification
            data.update(snippet)
            data["thumbnail_url"] = default_thumbnail["url"]

            if status:
                data["status"] = status["privacyStatus"]

            if content_count_data:
                data["item_count"] = content_count_data["itemCount"]

            result.append(data)

        return result
