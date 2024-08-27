from datetime import timedelta

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Annotated
from bson.objectid import ObjectId

from .models.User import Token, User
from .models.Book import Book, ResponseBook
from .controller.Token import authenticate_user, create_access_token, get_current_active_user

from .database import collection

from dotenv import dotenv_values
config = dotenv_values(".env")


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


app = FastAPI()


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(config["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.post("/books", response_model=Book)
async def create_book(book: Book, current_user: Annotated[User, Depends(get_current_active_user)]):
    book_dict = book.model_dump()
    collection.insert_one(book_dict)
    return book


@app.get("/books", response_model=List[ResponseBook])
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


@app.get("/books/{book_id}", response_model=ResponseBook)
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
    

@app.put("/books/{book_id}")
async def update_book(book_id: str, book: Book, current_user: Annotated[User, Depends(get_current_active_user)]):
    book_dict = book.model_dump()
    collection.update_one({"_id": ObjectId(book_id)}, {"$set": book_dict})
    return book


@app.delete("/books/{book_id}")
async def delete_book(book_id: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    collection.delete_one({"_id": ObjectId(book_id)})
    return {"message": "Book deleted successfully!"}

