import pytube


def get_youtube_audio_stream_url(video_url):
    """
    Accepts a YouTube video URL and returns the audio stream URL.
    """
    try:
        yt = pytube.YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        if audio_stream:
            return audio_stream.url
    except Exception:
        return None
