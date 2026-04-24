from fastapi import APIRouter, Depends, HTTPException, status
from models.schemas import (
    AIAnalyzeImageRequest, AIAnalyzeImageResponse,
    AIGenerateConclusionRequest, AIGenerateConclusionResponse,
    AIOCRRequest, AIOCRResponse, CategoryResponse
)
from typing import List
from utils.auth import get_current_user, CurrentUser
from utils.database import supabase
from services.openai_service import OpenAIService
from services.ocr_service import OCRService

router = APIRouter(tags=["ai"])

@router.post("/api/ai/analyze-image", response_model=AIAnalyzeImageResponse)
def analyze_image(
    payload: AIAnalyzeImageRequest,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Sends the image URL to OpenAI Vision API to generate a professional technical description.
    Updates the database record with the generated description.
    """
    try:
        # Fetch image URL and ensure owner access
        image_check = supabase.table("images") \
            .select("*, reports(user_id)") \
            .eq("id", str(payload.image_id)) \
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
            
        img_record = image_check.data[0]
        image_url = img_record.get("image_url")
        
        # Generate description using AI
        ai_description = OpenAIService.generate_image_description(payload.category, image_url)
        
        # Save to database
        supabase.table("images") \
            .update({"ai_description": ai_description, "category": payload.category}) \
            .eq("id", str(payload.image_id)) \
            .execute()
            
        return AIAnalyzeImageResponse(image_id=payload.image_id, description=ai_description)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI generation failed: {str(e)}"
        )

@router.post("/api/ai/generate-conclusion", response_model=AIGenerateConclusionResponse)
def generate_conclusion(
    payload: AIGenerateConclusionRequest,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Gathers all descriptions from images in the report, feeds them to GPT-4o,
    and returns a summary conclusion text. Updates the report's conclusion field.
    """
    try:
        # Verify ownership
        report_check = supabase.table("reports").select("user_id").eq("id", str(payload.report_id)).execute()
        if not report_check.data or report_check.data[0].get("user_id") != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Report does not exist or permission denied."
            )
            
        # Get all images for this report
        images_response = supabase.table("images").select("ai_description, edited_description").eq("report_id", str(payload.report_id)).execute()
        
        descriptions = []
        for img in (images_response.data or []):
            desc = img.get("edited_description") or img.get("ai_description")
            if desc:
                descriptions.append(desc)
                
        # Generate conclusion using AI
        conclusion = OpenAIService.generate_conclusion(descriptions)
        
        # Save to database
        supabase.table("reports") \
            .update({"conclusion": conclusion}) \
            .eq("id", str(payload.report_id)) \
            .execute()
            
        return AIGenerateConclusionResponse(conclusion=conclusion)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI conclusion compilation failed: {str(e)}"
        )

@router.post("/api/ai/ocr", response_model=AIOCRResponse)
def run_ocr(
    payload: AIOCRRequest,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Extracts text from the photo using PaddleOCR. Updates the image's ocr_text field.
    """
    try:
        # Fetch image URL and ensure owner access
        image_check = supabase.table("images") \
            .select("*, reports(user_id)") \
            .eq("id", str(payload.image_id)) \
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
            
        img_record = image_check.data[0]
        image_url = img_record.get("image_url")
        
        # Run OCR
        ocr_text = OCRService.extract_text(image_url)
        
        # Save to database
        supabase.table("images") \
            .update({"ocr_text": ocr_text}) \
            .eq("id", str(payload.image_id)) \
            .execute()
            
        return AIOCRResponse(image_id=payload.image_id, ocr_text=ocr_text)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OCR execution failed: {str(e)}"
        )

@router.get("/api/categories", response_model=List[CategoryResponse])
def get_categories(current_user: CurrentUser = Depends(get_current_user)):
    """
    Returns all categories for inspection photos.
    """
    try:
        response = supabase.table("categories").select("*").order("name").execute()
        return response.data or []
    except Exception as e:
        # Return fallback categories list if database call fails during bootstrapping
        fallback = [
            {"id": "c1111111-1111-1111-1111-111111111111", "name": "Gutter Blockage", "description": "Debris and blockages in gutter systems", "created_at": "2026-05-26T12:00:00Z"},
            {"id": "c2222222-2222-2222-2222-222222222222", "name": "Roof Defect", "description": "Damage or defects on roofing materials", "created_at": "2026-05-26T12:00:00Z"},
            {"id": "c3333333-3333-3333-3333-333333333333", "name": "Water Damage", "description": "Signs of water infiltration or damage", "created_at": "2026-05-26T12:00:00Z"},
            {"id": "c4444444-4444-4444-4444-444444444444", "name": "Structural Issue", "description": "Structural concerns or damage", "created_at": "2026-05-26T12:00:00Z"},
            {"id": "c5555555-5555-5555-5555-555555555555", "name": "Siding Damage", "description": "Damage to exterior siding", "created_at": "2026-05-26T12:00:00Z"},
            {"id": "c6666666-6666-6666-6666-666666666666", "name": "Foundation Issue", "description": "Foundation cracks or concerns", "created_at": "2026-05-26T12:00:00Z"},
            {"id": "c7777777-7777-7777-7777-777777777777", "name": "Electrical Hazard", "description": "Electrical safety issues", "created_at": "2026-05-26T12:00:00Z"},
            {"id": "c8888888-8888-8888-8888-888888888888", "name": "Plumbing Issue", "description": "Plumbing defects or leaks", "created_at": "2026-05-26T12:00:00Z"},
            {"id": "c9999999-9999-9999-9999-999999999999", "name": "HVAC Concern", "description": "Heating and cooling system issues", "created_at": "2026-05-26T12:00:00Z"},
            {"id": "caaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "name": "General Maintenance", "description": "General maintenance items", "created_at": "2026-05-26T12:00:00Z"}
        ]
        return fallback
