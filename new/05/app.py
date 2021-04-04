from flask import Flask, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate                   # albemic
from flask_admin import Admin                       # admin
from flask_admin.contrib.sqla import ModelView      # admin

from forms import NewCategoryForm, NewProductForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/ecoswap_database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'put some random string here'        # forms
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'                   # theme of admin pages

db = SQLAlchemy(app)

migrate = Migrate(app, db)                          # albemic

from models import Category, Product
from api import api                            # api
app.register_blueprint(api, url_prefix='/api')                  # api

admin = Admin(app, name='Ecoswap', template_mode='bootstrap3')    # admin, not pretty because causes dependencies
admin.add_view(ModelView(Category, db.session))                   # admin
admin.add_view(ModelView(Product, db.session))                    # admin

@app.route('/one_category')
def hello_world():
    category = Category.query.first()
    return category.name


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/products')
def list_books():
    products_by_category = {
        category: Product.query.filter(Product.category == category)
        for category in Category.query.all()
    }
    return render_template('products.html', categories=Category.query.all(), products_by_category=products_by_category)

@app.route('/new_category', methods=['GET', 'POST'])
def new_author():
    form = NewCategoryForm()
    if not form.validate_on_submit():
        return render_template('new_category.html', form=form)

    name = form.name.data.strip()

    if Category.query.filter(Category.name == name).count():
        flash(f'Error: {name} already exists')
        return render_template('new_category.html', form=form)

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    flash(f'New category {name} created')
    return redirect('/products')

@app.route('/new_product', methods=['GET', 'POST'])
def new_product():
    form = NewProductForm()
    if not form.validate_on_submit():
        return render_template('new_product.html', form=form)

    category = form.category.data.strip()
    name = form.name.data.strip()
    product_des = form.product_des.data.strip()

    if Product.query.filter(Product.name == name).count():
        flash(f'Error: {name} already exists')
        return render_template('new_product.html', form=form)

    if not Category.query.filter(Category.name == category).count():
        flash(f'Error: {name} needs existing category {category}')
        return render_template('new_product.html', form=form)

    product = Product(category=category, name=name, product_des=product_des)
    db.session.add(product)
    db.session.commit()
    flash(f'New product {name} created')
    return redirect('/products')


@app.route('/products_for_category')
def products_for_category():
    return render_template('products_for_category.html', categories=Category.query.all())