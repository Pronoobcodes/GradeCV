from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.cv import CV
    from app.models.job_description import JobDescription
    

class GradingResult(SQLModel, table=True):
    __tablename__ = "grading_results"

    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="users.id")
    cv_id: int = Field(index=True, foreign_key="cvs.id")
    job_description_id: int = Field(index=True, foreign_key="job_descriptions.id")

    score: float
    feedback: str
    raw_llm_response: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    owner: "User" = Relationship(back_populates="grade_reports")
    cv: "CV" = Relationship(back_populates="grade_reports")
    job_description: "JobDescription" = Relationship(back_populates="grade_reports")