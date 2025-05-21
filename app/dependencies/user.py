from fastapi import Depends
from app.repositories.impl.user_repository import UserRepository
from app.services.impl.user_service import UserService

def get_user_repository() -> UserRepository:
    return UserRepository()

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository=repo)