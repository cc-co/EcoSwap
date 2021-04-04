from app import db

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):                         # admin - rep of state of object
        return f'{self.name}'


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(Category)
    product_des = db.Column(db.String)

    def __repr__(self):
        return f'{self.name} by {self.category.name}'

    def as_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            price=self.price,
            category_id=self.category_id,
            product_des=self.product_des
        )