from rest_framework import status, views
from rest_framework.response import Response

from . import serializers
from .utils.youtube import YouTubeService


class ChannelSearch(views.APIView):
    """
    YouTube channels search by username
    returns only 10 most relevant results
    """

    def get(self, request, *args, **kwargs):
        username = request.query_params.get("username")

        if username:
            service = YouTubeService()
            channels_data = service.get_channels_data(username)
            if channels_data:
                serializer = serializers.ChannelSerializer(channels_data, many=True)
                return Response({"data": serializer.data})
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({"data": []})


class ChannelPlaylistsView(views.APIView):
    """
    Returns playlist sections of the channel.
    """

    def get(self, request, channel_id, *args, **kwargs):
        service = YouTubeService()
        playlists = service.get_playlists_by_channel_id(channel_id)
        if playlists:
            serializer = serializers.PlaylistSerializer(playlists, many=True)
            data = {
                "total": len(playlists),
                "items": serializer.data
            }
            return Response(data)
        return Response({"data": []})


class PlaylistVideosView(views.APIView):
    """
    Returns the playlist videos
    """

    def get(self, request, playlist_id, *args, **kwargs):
        service = YouTubeService()
        videos = service.get_playlist_videos(playlist_id)
        if videos:
            serializer = serializers.PlaylistVideoSerializer(videos, many=True)
            data = {
                "total": len(videos),
                "items": serializer.data
            }
            return Response(data)
        return Response({"data": []})


class VideoDetailsView(views.APIView):
    """
    Returns the video with its audio streaming link.
    """

    def get(self, request, video_id, *args, **kwargs):
        service = YouTubeService()
        video_list = service.get_video_detail(video_id)
        if video_list:
            video = video_list[0]
            serializer = serializers.VideoSerializer(video)
            return Response({"video": serializer.data})
        return Response(status=status.HTTP_404_NOT_FOUND)
