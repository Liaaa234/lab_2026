#dalle slides 06 PROGETTAZIONE WEB DINAMICO
from fastapi import FastAPI
from routers.books import books_router


app = FastAPI()

app.include_router(books_router)