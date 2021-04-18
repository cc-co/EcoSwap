from models import Author, Book, session

s = session()

for author in s.query(Author).order_by(Author.name):
    print(author.name)
    for book in s.query(Book).filter(Book.author == author).order_by(Book.year_of_publication):
        print(f'\t({book.year_of_publication}) {book.title}')
