import requests
from urllib.parse import urlparse
import os
import whisper
import warnings
from app.utils.utils import has_audio_stream

def get_loom_transcript(loom_url: str) -> str:
    try:
        warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

        path = urlparse(loom_url).path
        video_id = path.rstrip('/').split('/')[-1]

        if not video_id:
            raise ValueError("Video ID not found in Loom URL")

        api_url = f"https://www.loom.com/api/campaigns/sessions/{video_id}/transcoded-url"
        response = requests.post(api_url)

        if not response.ok:
            raise ValueError(f"Failed to fetch the video URL from Loom. Status code: {response.status_code}")

        video_url = response.json().get("url")
        if not video_url:
            raise ValueError("No video URL found in Loom API response.")

        output_file = f"video/loom_{video_id}.mp4"
        headers = { 'User-Agent': 'Mozilla/5.0' }

        if not os.path.exists(output_file):
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with requests.get(video_url, headers=headers, stream=True) as r:
                r.raise_for_status()
                with open(output_file, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

        if not has_audio_stream(output_file):
            os.remove(output_file)
            return "No audio stream found in Loom video — transcription not possible."

        model = whisper.load_model("base", device="cpu")
        result = model.transcribe(output_file, fp16=False)
        transcript = result.get("text", "")

        if os.path.exists(output_file):
            os.remove(output_file)

        return transcript

    except requests.RequestException as req_err:
        print(f"[ERROR] Request failed: {req_err}")
        raise ValueError(f"Request error: {req_err}")

    except (ValueError, KeyError, TypeError) as parse_err:
        print(f"[ERROR] Parsing failed: {parse_err}")
        raise ValueError(f"Parsing error: {parse_err}")
