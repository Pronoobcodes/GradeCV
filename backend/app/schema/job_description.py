from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class JobDescriptionCreate(BaseModel):
    title: Optional[str] = None
    content: str


class JobDescriptionRead(BaseModel):
    id: int
    title: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class JobDescriptionReadDetail(JobDescriptionRead):
    content: str