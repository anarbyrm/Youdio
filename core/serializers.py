from rest_framework import serializers


class ChannelSerializer(serializers.Serializer):
    channelId = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    thumbnail_url = serializers.URLField()


class PlaylistSerializer(serializers.Serializer):
    id = serializers.CharField()
    channelId = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    thumbnail_url = serializers.URLField()
    status = serializers.CharField()
    item_count = serializers.IntegerField(default=0)


class PlaylistVideoSerializer(serializers.Serializer):
    channelId = serializers.CharField()
    playlistId = serializers.CharField()
    video_id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    thumbnail_url = serializers.URLField()


class VideoSerializer(serializers.Serializer):
    id = serializers.CharField()
    channelId = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    audio_stream_url = serializers.URLField()
    thumbnail_url = serializers.URLField()
    view_count = serializers.IntegerField()
    like_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()
    publishedAt = serializers.DateTimeField()
