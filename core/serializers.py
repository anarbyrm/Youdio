from rest_framework import serializers


class ChannelSerializer(serializers.Serializer):
    kind = serializers.CharField()
    etag = serializers.CharField()
    channelId = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    thumbnail = serializers.URLField()


class PlaylistSerializer(serializers.Serializer):
    id = serializers.CharField()
    kind = serializers.CharField()
    etag = serializers.CharField()
    channelId = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    thumbnail = serializers.URLField()
    status = serializers.CharField()
    item_count = serializers.IntegerField()
