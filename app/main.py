#dalle slides 06 PROGETTAZIONE WEB DINAMICO
from fastapi import FastAPI
from routers.books import books_router
from contextlib import asynccontextmanager
from data.db import init_database   #prima che l'app sia disponibile viene chiamata questa funzione
from routers.users import users_router


#fa partire le cose prima che l'applicazione si avvii
@asynccontextmanager
async def lifespan(app: FastAPI):   #la prima volta che viene chiamata esegue le istruzioni prima di yield, la seconda volta che viene chiamata eseguirà quello che c'è dopo yield
    #on create
    init_database()
    yield
    #on close



app = FastAPI(lifespan=lifespan)

app.include_router(books_router)

app.include_router(users_router)
