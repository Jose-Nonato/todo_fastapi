from fastapi import FastAPI

from view.Book import book_router
from view.User import user_router

from dotenv import dotenv_values
config = dotenv_values(".env")


app = FastAPI()


app.router.include_router(user_router, tags=["User"])
app.router.include_router(book_router, tags=["Book"])
