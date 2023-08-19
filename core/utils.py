from typing import Any, Dict, List

from django.conf import settings
from googleapiclient.discovery import build

from .constants import SERVICE_NAME, VERSION, RequestType


def initiate_list_request(request_type: RequestType, **kwargs) -> Any:
    youtube = build(SERVICE_NAME, VERSION, developerKey=settings.YOUTUBE_API_KEY)

    if request_type == RequestType.SEARCH:
        request = youtube.search()
    elif request_type == RequestType.PLAYLISTS:
        request = youtube.playlists()
    return request.list(**kwargs)


def get_channels_data(username: str) -> str:
    try:
        searcher = initiate_list_request(
            RequestType.SEARCH,
            part="snippet",
            type="channel",
            maxResults=10,
            q=username,
        )
        channels_data = searcher.execute()
        prepared_channels = prepare_data(channels_data["items"])
        return prepared_channels
    except Exception as exp:
        return None


def get_playlists_by_channel_id(channel_id: str) -> List[Dict[str, Any]]:
    result = []

    next_page_token = None
    prev_page_token = None
    total = None
    count = 0
    limit = 50

    while True:
        try:
            if total and count >= total:
                break

            searcher = initiate_list_request(
                RequestType.PLAYLISTS,
                part="snippet",
                channelId=channel_id,
                maxResults=limit,
                nextPageToken=next_page_token,
                prevPageToken=prev_page_token,
            )
            playlists = searcher.execute()

            if not total:
                total = playlists["pageInfo"]["totalResults"]

            prepared_playlists = prepare_data(playlists["items"])
            result.append(prepared_playlists)
            count += limit

        except Exception as exp:
            return None


def prepare_data(data_list: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    This function modifies data to be ready for serialization.
    """
    result = []

    for data in data_list:
        snippet = data.pop("snippet")
        thumbnails = snippet.pop("thumbnails")
        default_thumbnail = thumbnails.get("default")

        # dictionary modification
        data.update(snippet)
        data["thumbnail_url"] = default_thumbnail["url"]
        result.append(data)

    return result
