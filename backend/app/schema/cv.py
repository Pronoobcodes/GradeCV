from datetime import datetime
from pydantic import BaseModel, Field


class CVRead(BaseModel):
    id: int
    file_name: str
    updated_at: datetime

    class Config:
        from_attributes = True


class CVReadDetail(CVRead):
    file_content: str
    
