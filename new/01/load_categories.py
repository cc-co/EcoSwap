from models import Category, Product, session


def load_lines(filename):
    with open(f'../data/{filename}') as input_file:
        lines = input_file.readlines()
    return [line.strip() for line in lines if line.strip()]


def load_data(session):
    s = session()
    s.query(Category).delete()
    s.query(Product).delete()

    # e.g. groceries
    category_lines = load_lines('category.txt')
    for line in category_lines:
        name = line
        name = name.strip()
        category = Category(name=name)
        s.add(category)

    # e.g. groceries|name|1
    product_lines = load_lines('products.txt')
    for line in product_lines:
        category_name, name, price = line.split('|')
        category_name, name, price = category_name.strip(), name.strip(), int(price)
        category = s.query(Category).filter(Category.name == category_name).one()
        product = Product(name=name, price=price, category=category)
        s.add(product)

    s.commit()


load_data(session)
