from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def extract_video_id(youtube_url: str) -> str:
    parsed_url = urlparse(youtube_url)
    if parsed_url.hostname in ["youtu.be"]:
        return parsed_url.path[1:]
    elif parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        query = parse_qs(parsed_url.query)
        return query.get("v", [None])[0]
    else:
        raise ValueError("Invalid YouTube URL")

def get_youtube_transcript(youtube_url: str) -> str:
    video_id = extract_video_id(youtube_url)
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = " ".join([entry['text'] for entry in transcript_list])
    return transcript_text

