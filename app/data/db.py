from click.types import convert_type
from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends
from schemas.book import BookDB     # noqa
from schemas.users import UserDB
from schemas.book_user_link import BookUserLink
from faker import Faker     #per il riempimento con i dati fittizi
import os

sqlite_file_name = "C:\\Users\\gika1\\lab_2026\\app\\data\\database.db"   #file persistente in memoria
sqlite_url = f"sqlite:///{sqlite_file_name}"    #file endpoint dove viene montato qualcosa(?)
engine = create_engine(
    sqlite_url, connect_args={"check_same_thread": False},
    echo=True
)

#inizializziamo il database
def init_database():
    ds_exists = os.path.isfile(sqlite_file_name)    #check per vedere se il file esiste già
    SQLModel.metadata.create_all(engine)
    if not ds_exists:                               #se non esiste utilizza faker per crearne uno con dati fittizi
        f = Faker("it_IT")
        with Session(engine) as session:
            for i in range(10):     #creo 10 libri
                book = BookDB(
                    title=f.sentence(nb_words=5),
                    author=f.name(),
                    review=f.pyint(1, 5),
                    user_id=f.pyint(1, 10)
                )
                session.add(book)
            for i in range(10):
                user = UserDB(
                    name=f.name(),
                    birth_date=f.date_of_birth(),
                    city=f.city()
                )
                session.add(user)
            for i in range(5):
                link = BookUserLink(
                    book_id=f.pyint(1, 10),
                    user_id=f.pyint(1, 10),
                )
                session.add(link)
            session.commit()

#dependecies
def get_session():
    with Session(engine) as session:      #passare il motore del database che è stato inizializzato
        yield session   #facendo yield la sessione rimane bloccata qui e ogni volta che chiamiamo la funzione riapre sempre la stessa istanza che è stata aperta in precedenza (?)

SessionDep = Annotated[Session, Depends(get_session)]  #salvo la dependen dentro una variabile per non riscriverla ogni volta