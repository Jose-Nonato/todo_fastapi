from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    description: str
    published_year: int

    class Config:
        schema_extra = {
            "example": {
                "title": "The Hitchhiker's Guide to the Galaxy",
                "author": "Douglas Adam",
                "description": "A humorous science fiction novel.",
                "published_year": 1979
            }
        }


class ResponseBook(BaseModel):
    id: str
    title: str
    author: str
    description: str
    published_year: int
