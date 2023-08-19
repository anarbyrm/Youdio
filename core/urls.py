from django.urls import path

from . import views

urlpatterns = [
    path("channels", views.ChannelSearch.as_view(), name="channel-search"),
    path("channels/<str:channel_id>/playlists", views.ChannelPlaylistsView.as_view(), name="playlist-list"),
    path("playlists/<str:playlist_id>/videos", views.PlaylistVideosView.as_view(), name="playlist-detail"),
]
