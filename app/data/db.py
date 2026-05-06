from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends

sqlite_file_name = "C:\\Users\\gika1\\lab_2026\\app\\data\\database.db"   #file persistente in memoria
sqlite_url = f"sqlite:///{sqlite_file_name}"    #file endpoint dove viene montato qualcosa(?)
engine = create_engine(
    sqlite_url, connect_args={"check_same_thread": False},
    echo=True
)

#inizializziamo il database
def init_database():
    SQLModel.metadata.create_all(engine)

#dependecies
def get_session():
    with Session(engine) as session:      #passare il motore del database che è stato inizializzato
        yield session   #facendo yield la sessione rimane bloccata qui e ogni volta che chiamiamo la funzione riapre sempre la stessa istanza che è stata aperta in precedenza (?)

SessionDep = Annotated[Session, Depends(get_session)]  #salvo la dependen dentro una variabile per non riscriverla ogni volta