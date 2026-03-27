from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated    #lo usiamo nei typing
from pydantic import Field, BaseModel

class Product(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=30)]    #li metto opzionali, ossia se non li passo non mi dà errore, se invece li passo allora vengono usati perchè
    price: Annotated[float, Field(gt=0)]                        #c'è | (or) quindi funziona sia se metto un valore sia se non lo metto con float | None = None
    location: Annotated[str, Field(min_length=3)]               #ora stiamo usando Annotated quindi non serve metterle opzionali

"""   
product = Product.model_validate(   #questa funzione prende un dizionario e lo trasforma in un oggetto di tipo Product, se il dizionario non rispetta le regole di validazione allora viene sollevata un'eccezione
    {"name": "Notebook DELL", "price": 2999.99, "location": "Cagliari"}
)
"""

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates= Jinja2Templates(directory="templates")

product_list = [
    {"name": "Notebook DELL", "price": 2999.99, "location": "Cagliari"},
    {"name": "Notebook HP", "price": 1999.99, "location": "Sassari"},
    {"name": "Notebook ASUS", "price": 1499.99, "location": "Samatzai"},
    {"name": "Notebook ACER", "price": 999.99, "location": "Fanculo"},
]
@app.get("/", response_class=HTMLResponse)#per aggiungere questa funzione all'endpoint dobbiamo mettere un decoratore, inzia con @ poi la variabile a cui si riferisce e poi il metodo e tra parentesi il percorso
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

@app.get("/product_form", response_class=HTMLResponse)
def add_product(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="product_form.html",
    )

@app.post("/insert_product")
def insert_product(
        product: Annotated[Product, Form()]
):
        product_list.append(product.model_dump())
        return "Product added successfully"

@app.post("/insert_product_json")
def insert_product_json(
        product: Product
):
    print(product)