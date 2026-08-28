from datetime import datetime
from pydantic import BaseModel


class GradingResultCreate(BaseModel):
    cv_id: int
    job_description_id: int


class GradingResultRead(BaseModel):
    id: int
    cv_id: int
    job_description_id: int
    score: float
    feedback: str
    created_at: datetime

    class Config:
        from_attributes = True