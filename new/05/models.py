from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):                         # admin - rep of state of object
        return f'{self.name}'


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(Category)
    product_des = db.Column(db.String)

    def __repr__(self):
        return f'{self.name} : {self.category.name} : {self.product_des} : £{self.price} '

    def as_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            price=self.price,
            category_id=self.category_id,
            product_des=self.product_des
        )


class User(UserMixin, db.Model):                                        # UserMixin provides a common interface needed to implement with Flask-Login
    __tablename__ = 'user'                                                              # can be used to check whether users are active
    id = db.Column(db.Integer, primary_key=True,unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    # role = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))
    # search_results = db.relationship('Search_result', backref='User', lazy="dynamic")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader                                                  # user_loader sets callback for reloading a user from session
def load_user(id):                                                  # can be called to load user given id
    return User.query.get(int(id))

# class Search_result(db.Model):
#     __tablename__ = 'search_result'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
#     category = db.relationship(Category)
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
#     query_result = db.Column(db.String(200), index=True, unique=True)
#     keywords = db.Column(db.String(200), index=True, unique=False)
#     created_at=db.Column(db.DateTime,index=True, default=datetime.utcnow)


class Post(db.Model):
    __tablename__ = 'posts'
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), index=True)
    date_posted=db.Column(db.DateTime,index=True, default=datetime.utcnow)
    content=db.Column(db.Text, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"