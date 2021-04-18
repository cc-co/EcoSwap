from models import Author, Book, session


def load_lines(filename):
    with open(f'../data/{filename}') as input_file:
        lines = input_file.readlines()
    return [line.strip() for line in lines if line.strip()]


def load_data(session):
    s = session()
    s.query(Author).delete()
    s.query(Book).delete()

    # e.g. Ursula K. Le Guin|1929
    author_lines = load_lines('authors.txt')
    for line in author_lines:
        name, year = line.split('|')
        name, year = name.strip(), int(year)
        author = Author(name=name, year_of_birth=year)
        s.add(author)

    # e.g. Ursula K. Le Guin|A Wizard of Earthsea|1968
    book_lines = load_lines('books.txt')
    for line in book_lines:
        author_name, title, year = line.split('|')
        author_name, title, year = author_name.strip(), title.strip(), int(year)
        author = s.query(Author).filter(Author.name == author_name).one()
        book = Book(title=title, year_of_publication=year, author=author)
        s.add(book)

    s.commit()


load_data(session)
