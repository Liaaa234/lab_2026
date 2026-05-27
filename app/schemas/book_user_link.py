from sqlmodel import SQLModel, Field

class BookUserLink(SQLModel, table=True):
    book_id: int = Field(foreign_key='bookdb.id', primary_key=True)
    user_id: int = Field(foreign_key='userdb.id', primary_key=True)

