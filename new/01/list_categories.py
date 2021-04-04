from models import Category, Product, session

s = session()

for category in s.query(Category).order_by(Category.name):
    print(category.name)
    for product in s.query(Product).filter(Product.category == category).order_by(Product.price):
        print(f'\t({product.price}) {product.name}')
