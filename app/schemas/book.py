#STRUTTURA DATI PER L'OGGETTO LIBRO

from typing import Annotated
from sqlmodel import SQLModel, Field

"""class BookPatch(BaseModel):
    title: str | None = None
    author: str | None = None
"""

"""class Book(BaseModel):
    id: int
    title: str
    author: str
    #review: int = None         il campo review ora diventa opzionale mettendo un valore di default (None)
    review: Annotated[int, Field(ge=1, le=5)] = None
"""

class BookBase(SQLModel):     #sarà la mia radice e avrà gli attributi che sono comuni a tutte e 4 le classi
    title: str
    author: str
    review: Annotated[int, Field(ge=1, le=5)] = None

#usarlo per la validazione dei dati (IMPORTANTE NEL PROGETTO)
class BookCreate(BookBase):   #solo titolo autore opzionale, la utilizziamo nelle POST
    pass    #siccome ereditiamo da BookBase lascio vuoti i campi

class BookPublic(BookBase):   #restituita nel GET(ci dev'essere anche l'id, quindi qua lo definisco), avremo tutto
    id: int

class BookDB(BookBase, table=True):   #con il parametro table=True, avremo tutto ma con il parametro table, stabilisce il ponte tra il nostro codice python e il database
    id: int = Field(default=None, primary_key=True)     #vogliamo che l'id sia la chiave primaria e che sia assegnata automaticamente dal database

"""class Book(SQLModel, table=True):
    id: int
    title: str
    author: str
    #review: int = None         il campo review ora diventa opzionale mettendo un valore di default (None)
    review: Annotated[int, Field(ge=1, le=5)] = None

        model_config = {
        "json_schema_extra": {      #aggiunge modelli aggiuntivi agli attributi
            "examples": [   #possiamo mettere una lista di dizionari di schemi già riempiti
                {
                    "id": 1,
                    "title": "Il nome della Rosa",
                    "author": "Umberto Eco",
                    "review": 5
                }
            ]
        }
    }


books =  {
    0: Book(id=0, title="Il nome della Rosa", author="Umberto Eco", review=5),
    1: Book(id=1, title="Il gioco dei sei", author="Umberto Eco", review=1),
    2: Book(id=0, title="Il gioco dei sette", author="Maccio Capatonda", review=3)
}
"""