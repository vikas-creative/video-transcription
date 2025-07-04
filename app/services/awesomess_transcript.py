import requests
from urllib.parse import urlparse, parse_qs
import os
import whisper
from app.utils.utils import has_audio_stream

def get_awesomess_transcript(url: str) -> str:
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        key = query_params.get("key", [None])[0]
        video_id = parsed_url.path.strip("/").split("/")[-1]

        if not key or not video_id:
            raise ValueError("Missing 'key' or 'video_id' in URL")

        api_url = f"https://www.awesomescreenshot.com/api/v1/video/load_video?id={video_id}&key={key}"

        response = requests.get(api_url)
        response.raise_for_status()

        json_data = response.json()
        video_url = json_data.get("data", {}).get("video", {}).get("fileWebMURI")

        if not video_url:
            raise ValueError("fileWebMURI not found in response")

        output_file = f"video/video_{video_id}.webm"

        headers = {
            'User-Agent': 'Mozilla/5.0', 
        }

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
        result = model.transcribe(output_file,fp16=False)
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