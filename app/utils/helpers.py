import os
import uuid
import shutil
from fastapi import UploadFile

UPLOAD_DIR = "uploads"

async def save_upload_file(upload_file: UploadFile, destination_filename: str) -> str:
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
        
    file_path = os.path.join(UPLOAD_DIR, destination_filename)
    
    # UploadFile file is a SpooledTemporaryFile
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
        
    return file_path

def generate_unique_filename(original_filename: str) -> str:
    ext = original_filename.split('.')[-1] if '.' in original_filename else ''
    unique_id = uuid.uuid4().hex
    return f"{unique_id}.{ext}" if ext else unique_id
