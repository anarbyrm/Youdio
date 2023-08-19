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
    video_url = serializers.URLField()
    default_audio_language = serializers.CharField()
    thumbnail_url = serializers.URLField()
    view_count = serializers.IntegerField()
    like_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()
    published_at = serializers.DateTimeField()
