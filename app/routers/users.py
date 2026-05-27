from fastapi import APIRouter
from data.db import SessionDep
from schemas.users import UserDB, UserPublic    #importiamo i database
from sqlmodel import select

users_router = APIRouter(prefix="/users")     #sottopercorso dedicato a questa risorsa

@users_router.get("/")
def get_all_users(session: SessionDep) -> list[UserPublic]:
    """Returns all users"""
    users = session.exec(select(UserDB)).all()
    return users

@users_router.get("/{id}/books")