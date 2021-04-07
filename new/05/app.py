from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate                   # albemic
from flask_admin import Admin                       # admin
from flask_admin.contrib.sqla import ModelView      # admin
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from forms import NewCategoryForm, NewProductForm, NewUserForm, LoginForm, UpdateProduct, UpdateCategoryForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/ecoswap_database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'put some random string here'        # forms
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'                   # theme of admin pages


db = SQLAlchemy(app)

migrate = Migrate(app, db)                          # alembic
login = LoginManager(app)
login.login_view = 'login'

from models import Category, Product, User
from api import api                            # api
app.register_blueprint(api, url_prefix='/api')                  # api

admin = Admin(app, name='Ecoswap', template_mode='bootstrap3')    # admin, not pretty because causes dependencies
admin.add_view(ModelView(Category, db.session))                   # admin
admin.add_view(ModelView(Product, db.session))                    # admin
admin.add_view(ModelView(User, db.session))

# @app.route('/one_category')
# def hello_world():
#     category = Category.query.first()
#     return category.name


## HOMEPAGE FOR APP

@app.route('/')
def index():
    return render_template('index.html')

## ******************* USER LOGIN ********************* ##

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template('login.html', form=form)

    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
        flash('Invalid username or password')
        return redirect(url_for('login'))

    login_user(user)
    return redirect(url_for('index'))

## ******************* USER REGISTRATION **************** ##

# creating and reading new users for the site
@app.route('/register', methods=['GET', 'POST'])
def newuser():
    form=NewUserForm()
    if not form.validate_on_submit():
        return render_template('new_user.html', form=form)

    username = form.username.data.strip()
    email = form.email.data.strip()
    
    if User.query.filter(User.username == username).count():
        flash(f'Error: {username} user already exists')
        return render_template('new_user.html', form=form)

    if User.query.filter(User.email == email).count():
        flash(f'Error: {email} user email address already exists')
        return render_template('new_user.html', form=form)

    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash(f'New user {form.username.data} registered')
    return redirect('/login')

## ******************* ACCESSING PRODUCTS - FRONTEND ******************* ##

# list all products available
@app.route('/products')
@login_required
def list_products():
    products_by_category = {
        category: Product.query.filter(Product.category == category)
        for category in Category.query.all()
    }
    return render_template('products.html', categories=Category.query.all(), products_by_category=products_by_category)

# reading all the products in a category
@app.route('/products_for_category')
def products_for_category():
    return render_template('products_for_category.html', categories=Category.query.all())



## ************ CREATING PRODUCTS AND CATEGORIES ******* ##

# reading and creating new products in the database
@app.route('/new_product', methods=['GET', 'POST'])
def new_product():
    form = NewProductForm()
    if not form.validate_on_submit():
        return render_template('new_product.html', form=form)

    category = form.category.data.strip()
    name = form.name.data.strip()
    price = int(form.price.data)
    product_des = form.product_des.data.strip()

    if Product.query.filter(Product.name == name).count():
        flash(f'Error: {name} already exists')
        return render_template('new_product.html', form=form)

    prod_cat = Category.query.filter(Category.name == category).first()

    if not Category.query.filter(Category.name == category).count():
        flash(f'Error: {name} needs existing category {category}')
        return render_template('new_product.html', form=form)

    product = Product(category=prod_cat, name=name, product_des=product_des, price=price)
    db.session.add(product)
    db.session.commit()
    flash(f'New product {name} created')
    return redirect('/products')

 #Updating the product
 #@app.route('/new_product_update', methods=['GET','PUT'])
 #def update(id): 
 #    form = UpdateProduct()

#     # will have to read inputs on HTML page
#     # info the user wants updated
#     name = form.name.data.strip()
     #category_id = int(form.category_id.data)
#     price = int(form.price.data)
#     product_des = form.product_des.data.strip()

#     updatedproduct = Product.query.filter(Product.id == id).one()
#     # finding a product that matches product name inputted by user above
     #prod_cat = Category.query.filter(Category.name == category).first()
#     # finding a category that matches cat. name inputted above
    
#     if not name:
#         updatedproduct.name=name
#     if not category_id:
#         updatedproduct.category_id=category_id
#     if not 
     

#     updatedproduct = Product(name=name, product_des=product_des, price=price)
#     # reassignment of updated product?

#     db.session.add(updatedproduct)
#     db.session.commit()
#     flash(f'Product {name} edited')
#     return redirect('/products')
 
#     # starting the DB query
# #    qry = db.session.query(Product).filter(Product.id==id)
# #    product_to_update = qry.first()
# #    if product_to_update: # if there's a match
# #       try:
#         # overwrite product's info
#         # save edits

#         # if product does not exist
# #       except:
# #            return redirect('/new_product')
#     # return to page


# reading and creating new categories in the database
@app.route('/new_category', methods=['GET', 'POST'])
def new_category():
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


@app.route('/new_category_update', methods=['GET', 'PUT'])
def category_update(id):
    form=UpdateCategoryForm()

    name = form.name.data.strip()

    #updatedcategory = Category.query.filter(Category.name == name).one()
    category_to_update = Category.name.ilike(f"%{name}%").one().update({'name':name})
    # should pick out single category which is closest to input
    category_to_update.name = name

    updatedcategory = Category(name=name, id=id)
    # db.session.add(updatedcategory)

    db.session.commit()
    flash(f'Category {name} edited')
    return redirect('/products')


## ********** DELETING ENTRIES FROM DB ************ ##

@app.route('/delete_product', methods=['DELETE'])
def remove_product():
    name=request.form.get("name")
    category=Category.query.filter(name=name).first()
    db.session.delete(category)
    db.session.commit()
    flash(f'Category {name} deleted')
    return redirect ('/')

@app.route('/delete_category', methods=['DELETE'])
def remove_category():
    name=request.form.get("name") # string that the user passes through
    category=Category.query.filter(name=name).first()
    db.session.delete(category)
    db.session.commit()
    flash(f'Category {name} deleted')
    # return redirect ('/')

## ******************* USER LOGOUT **************** ##

# logging out of a session
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))