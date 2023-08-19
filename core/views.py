from rest_framework import status, views
from rest_framework.response import Response

from .serializers import ChannelSerializer, PlaylistSerializer
from .utils import YouTubeService


class ChannelSearch(views.APIView):
    """
    YouTube channels search by username
    """

    def get(self, request, *args, **kwargs):
        username = request.query_params.get("username", None)

        if username is not None:
            service = YouTubeService()
            channels_data = service.get_channels_data(username)
            if channels_data:
                serializer = ChannelSerializer(channels_data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ChannelPlaylistsView(views.APIView):
    """
    Returns playlist sections of the channel.
    """

    def get(self, request, channel_id, *args, **kwargs):
        service = YouTubeService()
        playlists = service.get_playlists_by_channel_id(channel_id)
        if playlists:
            serializer = PlaylistSerializer(playlists, many=True)
            data = {
                "total": len(playlists),
                "items": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class PlaylistVideosView(views.APIView):
    """
    Returns the playlist videos
    """

    def get(self, request, channel_id, playlist_id, *args, **kwargs):
        service = YouTubeService()
        pass
