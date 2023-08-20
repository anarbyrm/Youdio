from django.urls import path

from . import views

urlpatterns = [
    path("channels", views.ChannelSearch.as_view(), name="channel-search"),
    path("channels/<str:channel_id>/playlists", views.ChannelPlaylistsView.as_view(), name="playlists"),
    path("playlists/<str:playlist_id>/videos", views.PlaylistVideosView.as_view(), name="playlist-items"),
    path("videos/<str:video_id>", views.VideoDetailsView.as_view(), name="video-detail")
]
