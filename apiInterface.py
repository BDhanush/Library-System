from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy 
from multipledispatch import dispatch

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class BookModel(db.Model):                                      # database table for books (acts as library)
	title = db.Column(db.String(100), nullable=False)
	author = db.Column(db.String(100), nullable=False)
	ISBN = db.Column(db.Integer, primary_key=True)
	file_format = db.Column(db.String(100), nullable=True)

	def __repr__(self):
		return f"Book(title = {self.title}, author = {self.author}, ISBN = {self.ISBN}, file_format = {self.file_format})"

with app.app_context():
    db.create_all()

book_put_args = reqparse.RequestParser()
book_put_args.add_argument("title", type=str, help="title of the book is required", required=True)
book_put_args.add_argument("author", type=str, help="author of the book is required", required=True)
book_put_args.add_argument("ISBN", type=int, help="ISBN of the book is required", required=True)
book_put_args.add_argument("file_format", type=int, help="is not an ebook", required=False)

resource_fields = {
	"title": fields.String,
	"author": fields.String,
	"ISBN": fields.Integer,
	"file_format": fields.String
}

class BookEndpoint(Resource):
	def get(self):                                              # get method to list all books in library
		result = BookModel.query.all()
		all_books = []
		for i in result:										# representing books as lists to return
			all_books.append( [i.title,i.author,i.ISBN] )
			if ( i.file_format ):								
				all_books[-1].append( i.file_format )			# if it's a ebook add file format as well
		return all_books										# 2d list, list that contains book( in the form [title,author,ISBN,optional: file_format])
	
	# def get(self,book_title):
	# 	result = BookModel.query.filter_by(title = book_title).first()
	# 	if(not result):
	# 		abort(409, message=f"Book {book_title} not found")
	# 	return result

	@marshal_with(resource_fields)
	def put(self):                                              # put method to add Book, Book is passed as data 
		args = request.form
		# args = book_put_args.parse_args()
		result = BookModel.query.filter_by( ISBN = args["ISBN"] ).first()
		
		if result:												# if Book already in table
			abort(409, message=f"Book {args["ISBN"]} already present")

		book = BookModel( title=args["title"], author=args["author"], ISBN=args["ISBN"], file_format = args.get("file_format") )
		db.session.add(book)
		db.session.commit()
		return book

	def delete(self, book_ISBN):                                # delete method to delete a Book, Book ISBN is passed as an argument
		book = BookModel.query.filter_by(ISBN = book_ISBN).first()
		if(not book):											# if Book not present
			abort(409, message=f"Book {book_ISBN} not present in database")
		db.session.delete(book)
		db.session().commit()
		return {"message" : f"Book {book_ISBN} deleted"}, 200

# get and put method endpoint : "http://127.0.0.1:5000/BookEndpoint"
# delete method endpoint : "http://127.0.0.1:5000/BookEndpoint/BookISBN"
api.add_resource(BookEndpoint,"/BookEndpoint", "/BookEndpoint/<int:book_ISBN>")

if __name__ == "__main__":
    app.run(debug=True)

