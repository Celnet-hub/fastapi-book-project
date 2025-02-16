from typing import OrderedDict
from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
import httpx

from api.db.schemas import Book, Genre, InMemoryDB

router = APIRouter()

db = InMemoryDB()
db.books = {
    1: Book(
        id=1,
        title="The Hobbit",
        author="J.R.R. Tolkien",
        publication_year=1937,
        genre=Genre.SCI_FI,
    ),
    2: Book(
        id=2,
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        publication_year=1954,
        genre=Genre.FANTASY,
    ),
    3: Book(
        id=3,
        title="The Return of the King",
        author="J.R.R. Tolkien",
        publication_year=1955,
        genre=Genre.FANTASY,
    ),
}


@router.post("/", status_code=status.HTTP_201_CREATED, name="create_book")
async def create_book(request: Request, book: Book):

    # call the webhook function
    request_url = str(request.url)
    await call_webhook("Creating Book", f"{request_url} Post endpoint was called", "success")

    # add book
    db.add_book(book)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=book.model_dump()
    )


@router.get(
    "/", response_model=OrderedDict[int, Book], status_code=status.HTTP_200_OK, name = "get_all_books"
)
async def get_books(request: Request) -> OrderedDict[int, Book]:

    # call the webhook function
    request_url = str(request.url)
    await call_webhook("Getting All Books", f"{request_url} Get all books endpoint was called", "success")

    return db.get_books()

# get books by ID
@router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK, name="get_book")
async def get_book(requests: Request, book_id: int) -> Book:
    try:
        # call the webhook function
        request_url = str(requests.url)
        await call_webhook("Getting Book by ID", f"{request_url} Get book by ID endpoint was called", "success")

        return db.get_book(book_id).model_dump()
    except AttributeError:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Book not found."},
        )


# add tag to route
@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK, name="update_book")
async def update_book(requests: Request, book_id: int, book: Book) -> Book:
    # call the webhook function
    request_url = str(requests.url)
    await call_webhook("Updating Book", f"{request_url} Put endpoint was called", "success")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=db.update_book(book_id, book).model_dump(),
    )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, name="delete_book")
async def delete_book(requests: Request, book_id: int) -> None:

    # call the webhook function
    request_url = str(requests.url)
    await call_webhook("Deleting Book", f"{request_url} Delete endpoint was called","success")

    db.delete_book(book_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)


# create a function that calls telex  webhook.
async def call_webhook(event_name: str, message: str, status: str):
    webhook_baseurl = "https://ping.telex.im/v1/webhooks/01950cf0-02ed-7989-a383-98d5684f5aea"
    event_name = event_name
    message = message
    status = status
    username = "Books Inventory APP" 
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{webhook_baseurl}?event_name={event_name}&message={message}&status={status}&username={username}")
        print(response.json())
        # return response.json()


