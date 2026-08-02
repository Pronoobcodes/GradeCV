from datetime import datetime, timezone
import uuid
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON
from typing import Any, Dict, List, Optional

class Grading(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    cv_id: uuid.UUID = Field(foreign_key="cv.id")
    user_id: uuid.UUID = Field(foreign_key="user.id")
    overall_score: int
    ats_score: int
    grammar_score: int
    formatting_score: int
    readability_score: int
    experience_score: int
    skills_score: int
    education_score: int
    
    strengths: List[str] = Field(default=[], sa_column=Column(JSON))
    weaknesses: List[str] = Field(default=[], sa_column=Column(JSON))
    missing_keywords: List[str] = Field(default=[], sa_column=Column(JSON))
    recommendations: List[str] = Field(default=[], sa_column=Column(JSON))
    ai_feedback: str
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
