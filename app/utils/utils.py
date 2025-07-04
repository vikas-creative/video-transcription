import subprocess
import json

def has_audio_stream(file_path: str) -> bool:
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "a",
            "-show_entries", "stream=codec_type",
            "-of", "json",
            file_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        probe = json.loads(result.stdout)
        return bool(probe.get("streams"))
    except Exception as e:
        print(f"[ERROR] ffprobe failed: {e}")
        return False
    
def detect_video_source(url: str) -> str:
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "loom.com" in url:
        return "loom"
    elif "awesomescreenshot.com" in url:
        return "awesomess"
    else:
        raise ValueError("Unsupported video source")    