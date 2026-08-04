from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict

class CVBase(BaseModel):
    original_filename: str
    file_type: str

class CVCreate(CVBase):
    stored_filename: str
    file_path: str
    extracted_text: str
    user_id: uuid.UUID

class CVResponse(CVBase):
    id: uuid.UUID
    user_id: uuid.UUID
    upload_date: datetime
    
    model_config = ConfigDict(from_attributes=True)

class CVResponseWithText(CVResponse):
    extracted_text: str
