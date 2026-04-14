from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime
from uuid import UUID

# --- Authentication ---
class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    email: str

# --- Categories ---
class CategoryResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# --- Images ---
class ImageCreate(BaseModel):
    report_id: UUID
    image_url: str
    filename: str
    category: Optional[str] = None
    ai_description: Optional[str] = None
    edited_description: Optional[str] = None
    ocr_text: Optional[str] = None
    upload_order: Optional[int] = 0

class ImageUpdate(BaseModel):
    category: Optional[str] = None
    ai_description: Optional[str] = None
    edited_description: Optional[str] = None
    ocr_text: Optional[str] = None
    upload_order: Optional[int] = None

class ImageResponse(BaseModel):
    id: UUID
    report_id: UUID
    image_url: str
    filename: str
    category: Optional[str] = None
    ai_description: Optional[str] = None
    edited_description: Optional[str] = None
    ocr_text: Optional[str] = None
    upload_order: Optional[int] = 0
    created_at: datetime

    class Config:
        from_attributes = True

# --- Reports ---
class ReportCreate(BaseModel):
    site_name: str
    client_name: str
    report_title: str
    inspection_date: date
    conclusion: Optional[str] = None
    status: Optional[str] = "draft"

class ReportUpdate(BaseModel):
    site_name: Optional[str] = None
    client_name: Optional[str] = None
    report_title: Optional[str] = None
    inspection_date: Optional[date] = None
    conclusion: Optional[str] = None
    pdf_url: Optional[str] = None
    status: Optional[str] = None

class ReportResponse(BaseModel):
    id: UUID
    user_id: UUID
    site_name: str
    client_name: str
    report_title: str
    inspection_date: date
    conclusion: Optional[str] = None
    pdf_url: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    images: Optional[List[ImageResponse]] = []

    class Config:
        from_attributes = True

# --- AI & OCR Endpoints Request/Response ---
class AIAnalyzeImageRequest(BaseModel):
    image_id: UUID
    category: str

class AIAnalyzeImageResponse(BaseModel):
    image_id: UUID
    description: str

class AIGenerateConclusionRequest(BaseModel):
    report_id: UUID

class AIGenerateConclusionResponse(BaseModel):
    conclusion: str

class AIOCRRequest(BaseModel):
    image_id: UUID

class AIOCRResponse(BaseModel):
    image_id: UUID
    ocr_text: str

class GeneratePDFRequest(BaseModel):
    report_id: UUID
