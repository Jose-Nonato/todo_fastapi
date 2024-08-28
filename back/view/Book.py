from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List

from bson.objectid import ObjectId

from database import collection
from models.User import User
from models.Book import Book, ResponseBook
from controller.Token import get_current_active_user
from controller.Book import BooksRepository

from dotenv import dotenv_values
config = dotenv_values(".env")


book_router = APIRouter()


@book_router.post("/books", response_model=Book)
async def create_book(book: Book, current_user: Annotated[User, Depends(get_current_active_user)]):
    response = BooksRepository.create_book(book)
    return response


@book_router.get("/books", response_model=List[ResponseBook])
async def get_books(current_user: Annotated[User, Depends(get_current_active_user)]):
    books = []
    for book in BooksRepository.find_all():
        book_data = {
            "id": str(book["_id"]),
            "title": book.get("title"),
            "author": book.get("author"),
            "description": book.get("description"),
            "published_year": book.get("published_year")
        }
        books.append(ResponseBook(**book_data))
    return books


@book_router.get("/books/{book_id}", response_model=ResponseBook)
async def get_book(book_id: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    book = BooksRepository.find_by_id(book_id)
    if book:
        book_data = {
            "id": str(book["_id"]),
            "title": book.get("title"),
            "author": book.get("author"),
            "description": book.get("description"),
            "published_year": book.get("published_year")
        }
        return ResponseBook(**book_data)
    else:
        raise HTTPException(status_code=404, detail="Book not found")
    

@book_router.put("/books/{book_id}")
async def update_book(book_id: str, book: Book, current_user: Annotated[User, Depends(get_current_active_user)]):
    response = BooksRepository.update_book(book_id, book)
    return response


@book_router.delete("/books/{book_id}")
async def delete_book(book_id: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    response = BooksRepository.delete_book(book_id)
    return response
