from fastapi import APIRouter, Depends, HTTPException, status, Response
from models.schemas import GeneratePDFRequest
from utils.auth import get_current_user, CurrentUser
from utils.database import supabase
from services.pdf_service import PDFService
from services.storage_service import StorageService

router = APIRouter(prefix="/api/pdf", tags=["pdf"])

@router.post("/generate", response_model=dict)
def generate_pdf_report(
    payload: GeneratePDFRequest,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Triggers PDF generation using ReportLab, uploads the PDF to storage,
    updates the report's pdf_url in Supabase, and returns the PDF URL.
    """
    try:
        # 1. Fetch report details (verify ownership)
        report_check = supabase.table("reports") \
            .select("*") \
            .eq("id", str(payload.report_id)) \
            .eq("user_id", current_user.id) \
            .execute()
            
        if not report_check.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found or access denied."
            )
            
        report_data = report_check.data[0]
        
        # 2. Fetch all images belonging to this report
        images_response = supabase.table("images") \
            .select("*") \
            .eq("report_id", str(payload.report_id)) \
            .order("upload_order") \
            .execute()
            
        images_list = images_response.data or []
        
        # 3. Generate PDF raw bytes
        pdf_bytes = PDFService.generate_report_pdf(report_data, images_list)
        
        # 4. Upload PDF to storage (Cloudinary or local)
        filename = f"inspection_report_{report_data.get('site_name', 'site').replace(' ', '_')}.pdf"
        pdf_url = StorageService.upload_pdf(pdf_bytes, filename)
        
        # 5. Update PDF URL and status in reports table
        supabase.table("reports") \
            .update({"pdf_url": pdf_url, "status": "completed"}) \
            .eq("id", str(payload.report_id)) \
            .execute()
            
        return {"pdf_url": pdf_url}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PDF Generation failed: {str(e)}"
        )

@router.get("/download/{report_id}")
def download_pdf_stream(
    report_id: str,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Convenience endpoint that directly downloads the PDF stream in the browser.
    """
    try:
        report_check = supabase.table("reports") \
            .select("*") \
            .eq("id", report_id) \
            .eq("user_id", current_user.id) \
            .execute()
            
        if not report_check.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found or access denied."
            )
            
        report_data = report_check.data[0]
        
        images_response = supabase.table("images") \
            .select("*") \
            .eq("report_id", report_id) \
            .order("upload_order") \
            .execute()
            
        images_list = images_response.data or []
        
        pdf_bytes = PDFService.generate_report_pdf(report_data, images_list)
        
        filename = f"inspection_report_{report_data.get('site_name', 'site').replace(' ', '_')}.pdf"
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to stream PDF: {str(e)}"
        )
