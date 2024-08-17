from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from models import Book, ResponseBook
from bson.objectid import ObjectId
from typing import List
import uvicorn
from dotenv import dotenv_values
config = dotenv_values(".env")


app = FastAPI()


client = MongoClient(config["MONGO_CONNECT"])
db = client[config["DB_NAME"]]
collection = db[config["COLLECTION"]]


@app.post("/books", response_model=Book)
async def create_book(book: Book):
    book_dict = book.model_dump()
    collection.insert_one(book_dict)
    return book


@app.get("/books", response_model=List[ResponseBook])
async def get_books():
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


@app.get("/books/{book_id}", response_model=ResponseBook)
async def get_book(book_id: str):
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
    

@app.put("/books/{book_id}")
async def update_book(book_id: str, book: Book):
    book_dict = book.model_dump()
    collection.update_one({"_id": ObjectId(book_id)}, {"$set": book_dict})
    return book


@app.delete("/books/{book_id}")
async def delete_book(book_id: str):
    collection.delete_one({"_id": ObjectId(book_id)})
    return {"message": "Book deleted successfully!"}

