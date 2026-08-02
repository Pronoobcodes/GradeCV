import uuid
from typing import Optional, List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.cv import CV
from app.schemas.cv import CVCreate

class CVRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, cv_id: uuid.UUID) -> Optional[CV]:
        return await self.session.get(CV, cv_id)

    async def get_user_cvs(self, user_id: uuid.UUID) -> List[CV]:
        statement = select(CV).where(CV.user_id == user_id)
        result = await self.session.exec(statement)
        return list(result.all())

    async def create(self, cv_in: CVCreate) -> CV:
        db_cv = CV(**cv_in.dict())
        self.session.add(db_cv)
        await self.session.commit()
        await self.session.refresh(db_cv)
        return db_cv
        
    async def delete(self, cv_id: uuid.UUID) -> bool:
        db_cv = await self.get_by_id(cv_id)
        if db_cv:
            await self.session.delete(db_cv)
            await self.session.commit()
            return True
        return False
