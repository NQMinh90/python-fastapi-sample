from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SQLAlchemySession # Đổi tên để tránh trùng
from typing import Generator
from app.core.config import settings

# Sử dụng URL từ settings, đảm bảo có connect_args cho SQLite
engine_args = {}
if settings.SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, **engine_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)