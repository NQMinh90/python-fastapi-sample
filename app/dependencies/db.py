from typing import Generator
from sqlalchemy.orm import Session as SQLAlchemySession

from app.db.session import SessionLocal # Import SessionLocal từ vị trí mới của nó

# Dependency để lấy DB session
def get_db() -> Generator[SQLAlchemySession, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()