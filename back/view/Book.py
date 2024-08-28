from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List

from bson.objectid import ObjectId

from database import collection
from models.User import User
from models.Book import Book, ResponseBook
from controller.Token import get_current_active_user

from dotenv import dotenv_values
config = dotenv_values(".env")


book_router = APIRouter()


@book_router.post("/books", response_model=Book)
async def create_book(book: Book, current_user: Annotated[User, Depends(get_current_active_user)]):
    book_dict = book.model_dump()
    collection.insert_one(book_dict)
    return book


@book_router.get("/books", response_model=List[ResponseBook])
async def get_books(current_user: Annotated[User, Depends(get_current_active_user)]):
    books = []
    for book in collection.find():
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
    book = collection.find_one({"_id": ObjectId(book_id)})
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
    book_dict = book.model_dump()
    collection.update_one({"_id": ObjectId(book_id)}, {"$set": book_dict})
    return book


@book_router.delete("/books/{book_id}")
async def delete_book(book_id: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    collection.delete_one({"_id": ObjectId(book_id)})
    return {"message": "Book deleted successfully!"}
