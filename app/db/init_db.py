import logging
from sqlmodel import SQLModel
from app.db.session import engine

logger = logging.getLogger(__name__)

async def init_db() -> None:
    # We are using Alembic for migrations, so create_all isn't strictly necessary for production,
    # but it can be used for initial setup if desired.
    # async with engine.begin() as conn:
    #     await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("Database initialized")
