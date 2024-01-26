import requests
import json

BASE_URL = "http://127.0.0.1:5000/"

class Book:
    def __init__(self, title:str, author:str, ISBN:int):                # initialize book with attributes
        if(type(title)!=str or type(author)!=str or type(ISBN)!=int):
            raise TypeError("Object attributes type mismatch")
        self.title = title
        self.author = author
        self.ISBN = ISBN
        
    def info(self):                                                     # function to display book info
        print(json.dumps(self.__dict__, indent=4))

    def to_json(self):
        return self.__dict__

class EBook(Book):
    def __init__(self, title:str, author:str, ISBN:int, file_format:str):
        if(type(file_format)!=str):
            raise TypeError("Object attributes type mismatch")
        super().__init__(title, author, ISBN)
        self.file_format = file_format
    

class Library():
    books = []
    
    def add_book(self,book):
        if(type(book)!=Book and type(book)!=EBook):
            raise TypeError("Can add only books or ebooks")
        self.books.append(book)


    def search_by_title(self,title:str):
        for book in self.books:
            if (book.title==title):
                return book
        return None
    
    def display_books(self):
        print(json.dumps([book.__dict__ for book in self.books], indent=4))

if __name__ == "__main__":
    book = Book("hi","hi",123)
    book1 = Book("hi1","hi1",1231)
    library = Library()
    library.add_book(book)
    library.add_book(book1)
    ebook = EBook("hi2","hi2",1232,"hi2")
    library.add_book(ebook)
    book_searched = library.search_by_title("hi1")
    # book_searched.info()
    # print()
    # library.display_books()
    response_ebook = requests.put(BASE_URL + "BookEndpoint", ebook.to_json())
    print(response_ebook.json())

    response_book = requests.put(BASE_URL + "BookEndpoint", book.to_json())
    print(response_book.json())

    response_book1 = requests.put(BASE_URL + "BookEndpoint", book1.to_json())
    print(response_book1.json())

    response_del = requests.delete(BASE_URL + "BookEndpoint/" + str(book1.ISBN))

    print(response_del.json())

    response_list = requests.get(BASE_URL + "BookEndpoint")
    print(response_list.json())

    

