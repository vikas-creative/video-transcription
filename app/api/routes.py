from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from app.services.youtube_transcript import get_youtube_transcript
from app.services.loom_transcript import get_loom_transcript
from app.services.awesomess_transcript import get_awesomess_transcript
from app.utils.utils import detect_video_source

router = APIRouter()

class TranscriptionRequest(BaseModel):
    url: HttpUrl

@router.post("/transcribe")
async def transcribe_video(request: TranscriptionRequest):
    try:
        url = str(request.url)
        source = detect_video_source(url)

        if source == "youtube":
            transcript = get_youtube_transcript(url)
        elif source == "loom":
            transcript = get_loom_transcript(url)
        elif source == "awesomess":
            transcript = get_awesomess_transcript(url)
        else:
            raise HTTPException(status_code=400, detail="Unsupported video source")

        return {"source": source, "transcript": transcript}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException as http_exc:
        print(f"http_exc: {http_exc}")
        raise http_exc
    except Exception as e:
        print(f"e: {e}")
        raise HTTPException(status_code=500, detail=f"Error while transcribing video: {str(e)}")

