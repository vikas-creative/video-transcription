from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from app.services.youtube_transcript import get_youtube_transcript
from app.services.loom_transcript import get_loom_transcript
from app.services.awesomess_transcript import get_awesomess_transcript

router = APIRouter()

class TranscriptionRequest(BaseModel):
    url: HttpUrl
    source: str 

@router.post("/transcribe")
async def transcribe_video(request: TranscriptionRequest):
    try:
        if request.source == "youtube":
            transcript = get_youtube_transcript(str(request.url))
            return {"source": "youtube", "transcript": transcript}

        elif request.source == "loom":
            transcript = get_loom_transcript(str(request.url))
            return {"source": "loom", "transcript": transcript}
        
        elif request.source == "awesomess":
            transcript = get_awesomess_transcript(str(request.url))
            return  {"source": "awesomess", "transcript": transcript}

        else:
            raise HTTPException(status_code=400, detail="Unsupported video source")

    except HTTPException as http_exc:
        print(f"http_exc:{http_exc}")
        raise http_exc
    except Exception as e:
        print(f"e:{e}")
        raise HTTPException(status_code=500, detail=f"Error while transcribing video: {str(e)}")

