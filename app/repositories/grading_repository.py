import uuid
from typing import Optional, List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.grading import Grading
from app.schemas.grading import GradingCreate

class GradingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, grading_id: uuid.UUID) -> Optional[Grading]:
        return await self.session.get(Grading, grading_id)

    async def get_by_cv_id(self, cv_id: uuid.UUID) -> List[Grading]:
        statement = select(Grading).where(Grading.cv_id == cv_id)
        result = await self.session.exec(statement)
        return list(result.all())

    async def get_user_gradings(self, user_id: uuid.UUID) -> List[Grading]:
        statement = select(Grading).where(Grading.user_id == user_id).order_by(Grading.created_at.desc())
        result = await self.session.exec(statement)
        return list(result.all())

    async def create(self, grading_in: GradingCreate) -> Grading:
        db_grading = Grading(**grading_in.dict())
        self.session.add(db_grading)
        await self.session.commit()
        await self.session.refresh(db_grading)
        return db_grading
