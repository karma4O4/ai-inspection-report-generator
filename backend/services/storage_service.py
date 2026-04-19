import os
import shutil
import uuid
from fastapi import UploadFile
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

# Setup Cloudinary config if available
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

cloudinary_enabled = False
if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
    try:
        cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET,
            secure=True
        )
        cloudinary_enabled = True
    except Exception as e:
        print(f"Error configuring Cloudinary: {e}")

# Base folder for local uploads fallback
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

class StorageService:
    @staticmethod
    def upload_image(file: UploadFile) -> str:
        """
        Uploads image file to Cloudinary. If credentials are not provided or error occurs,
        falls back to saving locally in the fastapi static uploads folder and returning a local URL.
        """
        filename = f"{uuid.uuid4()}_{file.filename.replace(' ', '_')}"
        
        # 1. Cloudinary upload
        if cloudinary_enabled:
            try:
                # Seek to start of file before upload
                file.file.seek(0)
                result = cloudinary.uploader.upload(
                    file.file,
                    public_id=f"inspection_reports/{uuid.uuid4()}",
                    overwrite=True,
                    resource_type="image"
                )
                return result.get("secure_url")
            except Exception as e:
                print(f"Cloudinary upload failed: {e}. Falling back to local storage.")

        # 2. Local fallback storage
        local_path = os.path.join(UPLOAD_DIR, filename)
        file.file.seek(0)
        with open(local_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Return local path url
        return f"/static/uploads/{filename}"

    @staticmethod
    def upload_pdf(pdf_bytes: bytes, filename: str) -> str:
        """
        Uploads PDF to Cloudinary or falls back to local storage.
        """
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        if cloudinary_enabled:
            try:
                result = cloudinary.uploader.upload(
                    pdf_bytes,
                    public_id=f"inspection_reports/pdf/{uuid.uuid4()}",
                    overwrite=True,
                    resource_type="raw"
                )
                return result.get("secure_url")
            except Exception as e:
                print(f"Cloudinary PDF upload failed: {e}. Falling back to local storage.")
                
        local_path = os.path.join(UPLOAD_DIR, unique_filename)
        with open(local_path, "wb") as buffer:
            buffer.write(pdf_bytes)
            
        return f"/static/uploads/{unique_filename}"
