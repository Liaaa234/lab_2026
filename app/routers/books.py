from fastapi import APIRouter, Path, HTTPException
from schemas.book import Book, books
from typing import Annotated
from schemas.review import Review   #importiamo la classe dall'altro file

books_router = APIRouter(prefix="/books", tags=["books"])

@books_router.get("/")
def get_all_books() -> list[Book]:
    """Returns the list ok available books."""
    return list(books.values())   #books.values è un generatore

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