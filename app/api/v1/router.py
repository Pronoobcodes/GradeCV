from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, cvs, grading, health

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(cvs.router, prefix="/cv", tags=["cv"])
api_router.include_router(grading.router, prefix="/grading", tags=["grading"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
