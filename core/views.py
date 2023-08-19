from rest_framework import status, views
from rest_framework.response import Response

from .serializers import ChannelSerializer
from .utils import get_channels_data


class ChannelSearch(views.APIView):
    """
    Search YouTube channels by username
    """

    def get(self, request, *args, **kwargs):
        username = request.query_params.get("username", None)
        # next_page_token = request.query_params.get('next_page_token', None)
        # prev_page_token = request.query_params.get('prev_page_token', None)

        if username:
            channels_data = get_channels_data(username)
            if channels_data:
                serializer = ChannelSerializer(channels_data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)


class ChannelDetailView(views.APIView):
    """
    It will return both video and playlist sections for the channel.
    """

    pass
