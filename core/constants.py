from enum import Enum

SERVICE_NAME = "youtube"
VERSION = "v3"


class RequestType(Enum):
    SEARCH = 0
    PLAYLISTS = 1
