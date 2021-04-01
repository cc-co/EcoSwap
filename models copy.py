from datetime import datetime
from app import db

class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    role = db.Column(db.String())
    search_history_id = db.Column(db.Integer, db.ForeignKey('search_result.id'))
    search_result = db.relationship(Search_result)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    category=db.Column(db.String(200),index=True, unique=True)
    price=db.Column(db.Integer)
    status=db.Column(db.String(200), index=True, unique=True)
    created_at=db.Column(db.DateTime,index=True, default=datetime.utcnow)


products_category = Table(
    "products_category",
    Base.metadata,
    Column("product_id,", Integer, ForeignKey("Product.product_id")),
    Column("category_id", Integer, ForeignKey("Category.category_id"))
)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    products_id = db.Column(db.String, db.ForeignKey('product.id'))

class Search_result(db.Model):
    __tablename__ = 'search_result'
    id = db.Column(db.Integer, primary_key=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(Category)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_names = db.Column(db.String(200), index=True, unique=True)
    keywords = db.Column(db.String(200), index=True, unique=False)
    created_at=db.Column(db.DateTime,index=True, default=datetime.utcnow)


engine = create_engine('sqlite:///./ecoswap_database.sqlite')

session = sessionmaker()

session.configure(bind=engine)
