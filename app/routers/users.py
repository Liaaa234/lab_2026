from fastapi import APIRouter, HTTPException
from data.db import SessionDep
from schemas.users import UserDB, UserPublic    #importiamo i database
from schemas.book import BookDB, BookPublic
from schemas.book_user_link import BookUserLink
from sqlmodel import select

users_router = APIRouter(prefix="/users")     #sottopercorso dedicato a questa risorsa

@users_router.get("/")
def get_all_users(session: SessionDep) -> list[UserPublic]:
    """Returns all users"""
    users = session.exec(select(UserDB)).all()
    return users

@users_router.get("/{id}/books")
def get_user_books(
    id: int,
    session: SessionDep
) -> list[BookPublic]:
    """Returns all books held by the given user."""
    user = session.gat(UserDB, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    statement = select(BookDB).join(BookUserLink).where(BookUserLink.user_id == id)
    result = session.exec(statement).all()
    return result