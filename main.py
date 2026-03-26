from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates= Jinja2Templates(directory="templates")

product_list = [
    {"name": "notebook DELL", "price": 2999.99, "location": "Cagliari"},
    {"name": "notebook HP", "price": 1999.99, "location": "Sassari"},
    {"name": "notebook ASUS", "price": 1499.99, "location": "Samatzai"},
    {"name": "notebook ACER", "price": 999.99, "location": "Fanculo"},
]
@app.get("/", response_class=HTMLResponse)#per aggiungere questa funzione all'endpoint dobbiamo mettere un decoratore, inzia con @ poi la variabile a cui si riferisce e poi il .metodo e tra parentesi il percorso
def home (request: Request):

    return templates.TemplateResponse(
        request=request,
        name='home.html',
        context={"text": "Welcome to the store"}
    )

@app.get("/products", response_class=HTMLResponse)
def products(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={"product_list": product_list}
    )