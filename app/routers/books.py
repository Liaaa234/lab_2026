from fastapi import APIRouter, Path, HTTPException, Query
from schemas.book import Book, books
from typing import Annotated
from schemas.review import Review   #importiamo la classe dall'altro file


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
        sort: Annotated[bool, Query(description="Sort books by their review")] = False
) -> list[Book]:
    """Returns the list ok available books."""
    if sort:
        return sorted(books.values(), key=lambda book: book.review)    #key è il campo che dovrebbe usare per ordinare la lista, lamba functions verrà applicata a ogni elemento di questa lista
    else:                                     #lamba prendono un input e restituiscono un output (dato un libro, prende il campo review)
        return list(books.values())


@books_router.get("/{id}")    #una GET per prendere un libro specifico, per questo usiamo /{id}
def get_book_by_id(
        id: Annotated[int, Path(description="The ID of the book to retrieve")]      #parametro di percorso quindi mettiamo Path da fastapi
) -> Book:
    """Returns the book with the given id"""

    #risolviamo il problema degli errori intercettandoli prima che dia un internal server error (error 500)
    try:        #mettiamo dentro il TRY il pezzo di codice che spero funzioni
        return books[id]
    except KeyError:    #sto intercettando l'errore 404
        raise HTTPException(status_code=404, detail="Book not found")


#aggiungiamo l'ENDPOINT
@books_router.post("/{id}/review")
def add_review(
        id: Annotated[int, Path(description="The ID of the book to retrieve")],
        review: Review
):
    """Add review to the book with the given ID"""
    try:
        books[id].review = review.review
        return "Review added successfully"
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found")


@books_router.post("/")
def add_book(book: Book):
    """Adds a new book."""

    #aggiungiamo la verifica di un errore
    if book.id in books:
        raise HTTPException(status_code=403, detail="Book already exists")
    books[book.id] = book
    return "Book added successfully"


@books_router.put("/{id}")
def replace_book(
        id: Annotated[int, Path(description="The ID of the book to replace")],
        book: Book
):
    """Replaces the book with the given ID"""
    if not id in books:
        raise HTTPException(status_code=404, detail="Book not found")
    books[id] = book    #riassegno un nuovo valore, viene ridefinita la risorsa --- non la sto modificando, ma proprio cambiando


@books_router.delete("/")   #cancelliamo tutti i libri
def delete_all_books():
    """Deletes all the stored books"""
    books.clear()
    return "Books deleted successfully"


@books_router.delete("/{id}")   #cancelliamo un solo libro
def delete_book(
        id: Annotated[int, Path(description="The ID of the book to delete")],
):
    """Deletes the book with the given id"""
    if not id in books:
        raise HTTPException(status_code=404, detail="Book not found")
    del books[id]
    return "Book deleted successfully"