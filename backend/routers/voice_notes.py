from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from uuid import UUID
from models.schemas import ImageResponse
from utils.auth import get_current_user, CurrentUser
from utils.database import supabase
from services.whisper_service import WhisperService

router = APIRouter(prefix="/api/voice-notes", tags=["voice-notes"])

@router.post("/transcribe", response_model=ImageResponse)
async def transcribe_voice_note(
    image_id: UUID = Form(...),
    file: UploadFile = File(...),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Accepts an audio file upload (voice note), transcribes it using OpenAI Whisper API,
    and updates the specified image's edited_description field with the transcript.
    """
    # Validate extension
    allowed_extensions = ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]
    file_ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported audio format. Allowed: {', '.join(allowed_extensions)}"
        )
        
    try:
        # Verify image ownership through report join
        image_check = supabase.table("images") \
            .select("*, reports(user_id)") \
            .eq("id", str(image_id)) \
            .execute()
            
        if not image_check.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )
            
        report_user_id = image_check.data[0].get("reports", {}).get("user_id")
        if report_user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )
            
        # Read audio file bytes
        file_bytes = await file.read()
        
        # Transcribe
        transcript = WhisperService.transcribe_audio(file_bytes, file.filename)
        
        if not transcript:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Audio transcription returned empty text."
            )
            
        # Update image's edited_description
        response = supabase.table("images") \
            .update({"edited_description": transcript}) \
            .eq("id", str(image_id)) \
            .execute()
            
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update image with transcript."
            )
            
        return response.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice note transcription failed: {str(e)}"
        )
