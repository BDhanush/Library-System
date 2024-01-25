import requests
import json

BASE_URL = "http://127.0.0.1:5000/"

class Book:
    def __init__(self, title:str, author:str, ISBN:int):                # initialize book with attributes
        self.title = title
        self.author = author
        self.ISBN = ISBN
        
    def info(self):                                                     # function to display book info
        print(json.dumps(self.__dict__, indent=4))

class EBook(Book):
    def __init__(self, title:str, author:str, ISBN:int, fileFormat:str):
        super().__init__(title, author, ISBN)
        self.fileFormat = fileFormat
    

class Library():
    books = []

    def addBook(self,book:Book):
        self.books.append(book)
    def addBook(self,book:EBook):
        self.books.append(book)

    def searchByTitle(self,title:str):
        for book in self.books:
            if (book.title==title):
                return book
        return None
    
    def displayBooks(self):
        print(json.dumps([book.__dict__ for book in self.books], indent=4))

if __name__ == "__main__":
    book = Book("hi","hi",123)
    book1 = Book("hi1","hi1",1231)
    library = Library()
    library.addBook(book)
    library.addBook(book1)
    ebook = EBook("hi2","hi2",1232,"hi2")
    library.addBook(ebook)
    bookSearched = library.searchByTitle("hi1")
    bookSearched.info()
    print()
    library.displayBooks()

