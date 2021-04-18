from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/books_and_authors.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import Author, Book


@app.route('/one_author')
def hello_world():
    author = Author.query.first()
    return author.name


@app.route('/first_template')
def first_template():
    return render_template('sample.html')


@app.route('/books')
def list_books():
    books_by_author = {
        author: Book.query.filter(Book.author == author)
        for author in Author.query.all()
    }
    return render_template('books.html', authors=Author.query.all(), books_by_author=books_by_author)
