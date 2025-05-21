from fastapi import FastAPI
from app.api.endpoints import items as items_api # Import router từ items.py
from app.api.endpoints import auth as auth_api, users as users_api
from app.api.endpoints import candidate_tags as candidate_tags_api
from app.api.endpoints import job_post_tags as job_post_tags_api
from app.core.config import settings

# from app.db.base_class import Base # Bỏ comment nếu bạn có SQLAlchemy models
# from app.db.session import engine # Bỏ comment nếu bạn có SQLAlchemy models

# Nếu bạn có SQLAlchemy models và muốn tạo tables khi khởi động (chỉ cho development)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Một dự án FastAPI mẫu với kiến trúc 3 lớp và các lớp Base.",
    version="0.1.0",
)

# Include router của items vào ứng dụng chính với prefix /api/v1
app.include_router(items_api.router, prefix=settings.API_V1_STR)
app.include_router(auth_api.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(users_api.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
app.include_router(candidate_tags_api.router, prefix=settings.API_V1_STR) # Prefix và tags đã được định nghĩa trong router
app.include_router(job_post_tags_api.router, prefix=settings.API_V1_STR) # Prefix và tags đã được định nghĩa trong router

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}!"}