from sqlmodel import create_engine, SQLModel, Session

sqlite_file_name = "C:\\Users\\gika1\\lab_2026\\app\\data\\database.db"   #file persistente in memoria
sqlite_url = f"sqlite:///{sqlite_file_name}"    #file endpoint dove viene montato qualcosa(?)
engine = create_engine(
    sqlite_url, connect_args={"check_same_thread": False},
    echo=True
)

#inizializziamo il database
def init_database():
    SQLModel.metadata.create_all(engine)
