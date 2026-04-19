from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from models.schemas import ReportCreate, ReportUpdate, ReportResponse
from utils.auth import get_current_user, CurrentUser
from utils.database import supabase

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.post("", response_model=ReportResponse)
def create_report(report: ReportCreate, current_user: CurrentUser = Depends(get_current_user)):
    """
    Creates a new inspection report for the authenticated user.
    """
    try:
        report_data = report.model_dump()
        report_data["user_id"] = current_user.id
        
        response = supabase.table("reports").insert(report_data).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create report"
            )
            
        return response.data[0]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("", response_model=List[ReportResponse])
def list_reports(current_user: CurrentUser = Depends(get_current_user)):
    """
    Lists all reports belonging to the authenticated user.
    """
    try:
        response = supabase.table("reports") \
            .select("*, images(*)") \
            .eq("user_id", current_user.id) \
            .order("created_at", desc=True) \
            .execute()
            
        return response.data or []
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("/{id}", response_model=ReportResponse)
def get_report(id: UUID, current_user: CurrentUser = Depends(get_current_user)):
    """
    Retrieves a single inspection report by ID, with associated images.
    """
    try:
        response = supabase.table("reports") \
            .select("*, images(*)") \
            .eq("id", str(id)) \
            .eq("user_id", current_user.id) \
            .execute()
            
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
            
        report_data = response.data[0]
        # Sort images by upload_order if present
        if "images" in report_data and report_data["images"]:
            report_data["images"] = sorted(report_data["images"], key=lambda x: x.get("upload_order", 0) or 0)
            
        return report_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.put("/{id}", response_model=ReportResponse)
def update_report(id: UUID, report_update: ReportUpdate, current_user: CurrentUser = Depends(get_current_user)):
    """
    Updates an existing report.
    """
    try:
        # Check ownership
        check = supabase.table("reports").select("id").eq("id", str(id)).eq("user_id", current_user.id).execute()
        if not check.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found or permission denied"
            )
            
        update_data = {k: v for k, v in report_update.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No update fields provided"
            )
            
        response = supabase.table("reports").update(update_data).eq("id", str(id)).execute()
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.delete("/{id}")
def delete_report(id: UUID, current_user: CurrentUser = Depends(get_current_user)):
    """
    Deletes a report by ID.
    """
    try:
        # Check ownership
        check = supabase.table("reports").select("id").eq("id", str(id)).eq("user_id", current_user.id).execute()
        if not check.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found or permission denied"
            )
            
        supabase.table("reports").delete().eq("id", str(id)).execute()
        return {"status": "success", "message": "Report deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
