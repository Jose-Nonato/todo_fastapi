from fastapi import HTTPException
from database import collection
from models.Book import Book
from bson.objectid import ObjectId


class BooksRepository:
    @staticmethod
    def find_all():
        return collection.find()
    
    
    @staticmethod
    def find_by_id(book_id):
        query = collection.find_one({"_id": ObjectId(book_id)})
        if not query:
            return HTTPException(status_code=422, detail="Invalid ID item")
        return query
    

    @staticmethod
    def create_book(book: Book):
        try:
            book_dict = book.model_dump()
            collection.insert_one(book_dict)
            return book
        except:
            raise HTTPException(status_code=400, detail="Error in database")
        
    
    @staticmethod
    def delete_book(book_id):
        query = collection.find_one({"_id": ObjectId(book_id)})
        if query is not None:
            collection.delete_one({"_id": ObjectId(book_id)})
            return {"message": "Book deleted successfully!"}
        else:
            return {"message": "There is no book with this ID!"}
        
    
    @staticmethod
    def update_book(book_id, book: Book):
        query = collection.find_one({"_id": ObjectId(book_id)})
        if query is not None:
            book_dict = book.model_dump()
            collection.update_one({"_id": ObjectId(book_id)}, {"$set": book_dict})
            return {"book": book, "message": "Item updated successfully!"}
        else:
            return {"message": "There is no book with this ID!"}
