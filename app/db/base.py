# Import all the models, so that Base has them before being
# imported by Alembic
from sqlmodel import SQLModel

# Make sure all models are imported here or in __init__.py so Alembic can find them
from app.models.user import User
from app.models.cv import CV
from app.models.grading import Grading

# Base metadata for alembic
metadata = SQLModel.metadata
