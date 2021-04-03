from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Users(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    role = Column(String())
    search_history_id = Column(Integer, ForeignKey('search_result.id'))
    search_result = relationship('Search_result', backref='product', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    category=Column(String(200),index=True, unique=True)
    price=Column(Integer)
    status=Column(String(200), index=True, unique=True)
    created_at=Column(DateTime,index=True, default=datetime.utcnow)

# #Association table for "Many to many relationship" between products and categories
# products_category = Table(
#     "products_category",
#     Base.metadata,
#     Column("product_id,", Integer, ForeignKey("product.id")),
#     Column("category_id", Integer, ForeignKey("category.id"))
# )

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String())
    products_id = Column(String, ForeignKey('product.id'))



class Search_result(Base):
    __tablename__ = 'search_result'
    id = Column(Integer, primary_key=True)

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', backref='category', lazy=True)

    product_id = Column(Integer, ForeignKey('product.id'))
    product_names = Column(String(200), index=True, unique=True)
    products = relationship('Product', backref='product', lazy=True)

    keywords = Column(String(200), index=True, unique=False)
    created_at=Column(DateTime,index=True, default=datetime.utcnow)

engine = create_engine('sqlite:///./ecoswap_database.sqlite')

session = sessionmaker()

session.configure(bind=engine)
