from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from uuid import UUID
from typing import Optional
from models.schemas import ImageCreate, ImageUpdate, ImageResponse
from utils.auth import get_current_user, CurrentUser
from utils.database import supabase
from services.storage_service import StorageService

router = APIRouter(prefix="/api/images", tags=["images"])

@router.post("/upload", response_model=dict)
def upload_image_file(
    file: UploadFile = File(...),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Uploads an image file to Cloudinary (or local fallback storage).
    Validates file sizes (< 5MB) and formats (png, jpg, jpeg).
    """
    # Validate size (5MB = 5 * 1024 * 1024 bytes)
    max_size = 5 * 1024 * 1024
    
    # Read a chunk to see if size is within limits
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum limit of 5MB."
        )
        
    # Validate extensions
    allowed_extensions = ["png", "jpg", "jpeg"]
    file_ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PNG, JPG, and JPEG images are allowed."
        )
        
    try:
        url = StorageService.upload_image(file)
        return {"image_url": url, "filename": file.filename}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )

@router.post("", response_model=ImageResponse)
def save_image_metadata(
    image: ImageCreate,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Saves image metadata to the Supabase database.
    """
    try:
        # Check report ownership
        report_check = supabase.table("reports").select("user_id").eq("id", str(image.report_id)).execute()
        if not report_check.data or report_check.data[0].get("user_id") != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Report does not exist or permission denied."
            )
            
        image_data = image.model_dump()
        response = supabase.table("images").insert(image_data).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to save image metadata"
            )
            
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.put("/{id}", response_model=ImageResponse)
def update_image_metadata(
    id: UUID,
    image_update: ImageUpdate,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Updates category, descriptions, or OCR text of a specific image.
    """
    try:
        # Verify image ownership through report join
        image_check = supabase.table("images") \
            .select("*, reports(user_id)") \
            .eq("id", str(id)) \
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
            
        update_data = {k: v for k, v in image_update.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No update fields provided"
            )
            
        response = supabase.table("images").update(update_data).eq("id", str(id)).execute()
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.delete("/{id}")
def delete_image(
    id: UUID,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Deletes an image by ID.
    """
    try:
        # Verify image ownership
        image_check = supabase.table("images") \
            .select("*, reports(user_id)") \
            .eq("id", str(id)) \
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
            
        supabase.table("images").delete().eq("id", str(id)).execute()
        return {"status": "success", "message": "Image deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
