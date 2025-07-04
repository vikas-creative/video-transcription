import requests
from urllib.parse import urlparse, parse_qs

# https://www.awesomescreenshot.com/api/v1/video/load_video?id=29984315&key=56e0915033f19b126f9903de6c0dd881

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
            raise ValueError("webmOrigURI not found in response")

        output_file = "video_downloaded.mp4"

        headers = {
            'User-Agent': 'Mozilla/5.0', 
        }

        response = requests.get(video_url, headers=headers, stream=True)

        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print("Video downloaded successfully.")
        return video_url

    except requests.RequestException as req_err:
        print(f"[ERROR] Request failed: {req_err}")
        raise ValueError(f"Request error: {req_err}")

    except (ValueError, KeyError, TypeError) as parse_err:
        print(f"[ERROR] Parsing failed: {parse_err}")
        raise ValueError(f"Parsing error: {parse_err}")