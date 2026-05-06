from fastapi import APIRouter, Path, HTTPException, Query
from schemas.book import BookCreate, BookPublic, BookDB
from typing import Annotated
from schemas.review import Review   #importiamo la classe dall'altro file
from data.db import SessionDep
from sqlmodel import select, delete


books_router = APIRouter(prefix="/books", tags=["books"])

"""
@books_router.get("/")
def get_all_books() -> list[Book]:
    Returns the list ok available books.
    return list(books.values())   #books.values è un generatore
"""
#riscriviamo questa get con le query strings
@books_router.get("/")
def get_all_books(
        session: SessionDep,
        sort: Annotated[bool, Query(description="Sort books by their review")] = False
) -> list[BookPublic]:
    """Returns the list ok available books."""
    books = session.exec(select(BookDB)).all()      #.all per prendere la lista di tutti i libri
    if sort:
        return sorted(books, key=lambda book: book.review)    #key è il campo che dovrebbe usare per ordinare la lista, lamba functions verrà applicata a ogni elemento di questa lista
    else:                                     #lamba prendono un input e restituiscono un output (dato un libro, prende il campo review)
        return list(books)


@books_router.get("/{id}")    #una GET per prendere un libro specifico, per questo usiamo /{id}
def get_book_by_id(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the book to retrieve")]      #parametro di percorso quindi mettiamo Path da fastapi
) -> BookPublic:
    """Returns the book with the given id"""
    book = session.get(BookDB, id)      #gli passiamo la tabella e il valore della chiave primaria che vogliamo pescare

    """
    #risolviamo il problema degli errori intercettandoli prima che dia un internal server error (error 500)
    try:        #mettiamo dentro il TRY il pezzo di codice che spero funzioni
        return books[id]
    except KeyError:    #sto intercettando l'errore 404
        raise HTTPException(status_code=404, detail="Book not found")
    """
    #modificiamo la try di prima
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")

#aggiungiamo l'ENDPOINT
@books_router.post("/{id}/review")
def add_review(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the book to retrieve")],
        review: Review
):
    """Add review to the book with the given ID"""
    book = session.get(BookDB, id) #recuperiamo il libro tramite chiave primaria
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.review = review.review     #aggiorniamo il campo review
    session.add(book)   #reinseriamo la riga nel database
    session.commit()

    """     NON SERVONO PIù I TRY
    try:
        books[id].review = review.review
        return "Review added successfully"
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found")
    """


@books_router.post("/")
def add_book(session: SessionDep, book: BookCreate):
    """Adds a new book."""

    """     NON si verificherà mai questo problema perchè ADESSSO l'id viene generato dal sistema
    #aggiungiamo la verifica di un errore
    if book.id in books:
        raise HTTPException(status_code=403, detail="Book already exists")
    books[book.id] = book
    """
    book_entry = BookDB.model_validate(book)
    session.add(book_entry)
    session.commit()    #rendiamo effettive le modifiche al database
    return "Book added successfully"


@books_router.put("/{id}")
def replace_book(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the book to replace")],
        new_book: BookCreate
):
    """Replaces the book with the given ID"""
    book = session.get(BookDB, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.title = new_book.title
    book.author = new_book.author
    book.review = new_book.review
    session.add(book)   #stiamo riassegnando al database nella stessa riga(allo stesso id) l'oggetto aggiornato
    session.commit()
    return "Book replaced successfully"


@books_router.delete("/")   #cancelliamo tutti i libri
def delete_all_books(session: SessionDep):
    """Deletes all the stored books"""
    session.exec(delete(BookDB))
    session.commit()
    return "Books deleted successfully"


@books_router.delete("/{id}")   #cancelliamo un solo libro
def delete_book(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the book to delete")],
):
    """Deletes the book with the given id"""

    """
    if not id in books:
        raise HTTPException(status_code=404, detail="Book not found")
    del books[id]
    """
    book = session.get(BookDB, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)    #lavora a livello di istanza di una riga, NON di tutta la tabella
    session.commit()
    return "Book deleted successfully"