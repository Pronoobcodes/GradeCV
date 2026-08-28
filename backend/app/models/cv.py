from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.grading_result import GradingResult

    
class CV(SQLModel, table=True):
    __tablename__ = "cvs"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="users.id")
    filename: str
    file_content: str
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    owner: "User" = Relationship(back_populates="cvs")
    grade_reports: list["GradingResult"] = Relationship(back_populates="cv")