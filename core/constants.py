from enum import Enum

SERVICE_NAME = "youtube"
VERSION = "v3"
YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3/"
YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v={}"


class RequestType(Enum):
    SEARCH = 0
    PLAYLISTS = 1
    PLAYLIST_ITEMS = 2
