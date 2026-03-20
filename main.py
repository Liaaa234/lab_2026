from fastapi import FastAPI

app = FastAPI()   #tramite attraverso il quale interagiamo con l'applicazione (?)

@app.get("/")      #tra parentesi il percorso dell'end point (ora è sul percorso radice "/")
def hello_world():              #funzione classica, per farla diventare un end point bisogna aggiungere un decoratore
    return "Hello World!"   #per lanciare l'applicazione (?) si usa "fastapi dev" e scrivendo sul browser "localhost:8000" vediamo il risultato