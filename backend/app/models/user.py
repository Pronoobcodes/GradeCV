from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.cv import CV
    from app.models.job_description import JobDescription
    from app.models.grading_result import GradingResult
    

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    full_name: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    cvs: list["CV"] = Relationship(back_populates="owner")
    job_descriptions: list["JobDescription"] = Relationship(back_populates="owner")
    grade_reports: list["GradingResult"] = Relationship(back_populates="owner")