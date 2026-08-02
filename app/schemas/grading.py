from datetime import datetime
import uuid
from pydantic import BaseModel
from typing import List, Optional

class GradingBase(BaseModel):
    overall_score: int
    ats_score: int
    grammar_score: int
    formatting_score: int
    readability_score: int
    experience_score: int
    skills_score: int
    education_score: int
    
    strengths: List[str]
    weaknesses: List[str]
    missing_keywords: List[str]
    recommendations: List[str]
    ai_feedback: str

class GradingCreate(GradingBase):
    cv_id: uuid.UUID
    user_id: uuid.UUID

class GradingResponse(GradingBase):
    id: uuid.UUID
    cv_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
