from datetime import datetime, timezone
import uuid
from sqlmodel import SQLModel, Field
from typing import Optional

class CV(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    original_filename: str
    stored_filename: str
    file_path: str
    file_type: str
    extracted_text: str
    upload_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
