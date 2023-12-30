from typing import Optional
import pytube


def get_youtube_audio_stream_url(video_url: str) -> Optional[str]:
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


def get_video_url_from_youtube_page(html: str) -> Optional[str]:
    """
    Takes a YouTube page html source code string and returns the video url
    """
    from bs4 import BeautifulSoup

    try:
        soup = BeautifulSoup(html, "html.parser")
        video_url = soup.find("iframe")["src"].strip("/")
        return video_url
    except Exception:
        return None
