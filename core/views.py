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

        if not username:
            return Response({"data": []})

        try:
            service = YouTubeService()
            channels_data = service.get_channels_data(username)

            if not channels_data:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = serializers.ChannelSerializer(channels_data, many=True)
            return Response({"data": serializer.data})
        except Exception:
            return Response({"message": "An error occured during fetching channels."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChannelPlaylistsView(views.APIView):
    """
    Returns playlist sections of the channel.
    """

    def get(self, request, channel_id, *args, **kwargs):
        try:
            service = YouTubeService()
            playlists = service.get_playlists_by_channel_id(channel_id)

            if not playlists:
                return Response({"data": []})
            
            serializer = serializers.PlaylistSerializer(playlists, many=True)
            data = {
                "total": len(playlists),
                "items": serializer.data
            }
            return Response(data)
        except Exception:
            return Response({"message": "An error occured during fetching playlists for channels id %s." %(channel_id)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlaylistVideosView(views.APIView):
    """
    Returns the playlist videos
    """

    def get(self, request, playlist_id, *args, **kwargs):
        try:
            service = YouTubeService()
            videos = service.get_playlist_videos(playlist_id)

            if not videos:
                return Response({"data": []})

            serializer = serializers.PlaylistVideoSerializer(videos, many=True)
            data = {
                "total": len(videos),
                "items": serializer.data
            }
            return Response(data)
        except Exception:
            return Response({"message": "An error occured during fetching videos for playlist id %s." %(playlist_id)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VideoDetailsView(views.APIView):
    """
    Returns the video with its audio streaming link.
    """

    def get(self, request, video_id, *args, **kwargs):
        try:
            service = YouTubeService()
            video_list = service.get_video_detail(video_id)

            if not video_list:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = serializers.VideoSerializer(video_list[0])
            return Response({"video": serializer.data})
        except Exception as exc:
            return Response({"message": "Video with id %s cannot be fetched" %(video_id)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
