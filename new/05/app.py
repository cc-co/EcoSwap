from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate                   # albemic
from flask_admin import Admin                       # admin
from flask_admin.contrib.sqla import ModelView      # admin
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from forms import NewCategoryForm, NewProductForm, NewUserForm, PostForm, LoginForm, UpdateProduct, RemoveProduct, RemoveCategory, RemoveUser, RemovePost

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/ecoswap_database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'random string'                      # forms
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'                   # theme of admin pages


db = SQLAlchemy(app)

migrate = Migrate(app, db)                          # alembic
login = LoginManager(app)
login.login_view = 'login'

from models import Category, Product, User, Post
from api import api                            # api
app.register_blueprint(api, url_prefix='/api')                  # api

admin = Admin(app, name='Ecoswap', template_mode='bootstrap3')    # admin, not pretty because causes dependencies
admin.add_view(ModelView(Category, db.session))                   # admin
admin.add_view(ModelView(Product, db.session))                    # admin
admin.add_view(ModelView(User, db.session))                       # admin
admin.add_view(ModelView(Post, db.session))                       # admin

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

## ******************* DELETING USERS - BACKEND ******************* ##
@app.route('/users')
def list_users():
        for user in User.query.all():
            print(user)
        return "users :)"

@app.route('/delete_user', methods=['GET','POST'])
def remove_user():
    form = RemoveUser()

    if (request.method=='GET'):
        return render_template('delete_user.html', users=User.query.all(), form=form)
    else:

        if not form.validate_on_submit():
            return render_template('delete_user.html', form=form)
        
        name = request.form.get("name")                                       # string that the user passes through

        if not User.query.filter(User.username == name).count():
            flash(f'User "{name}" does not exist')
            return render_template('delete_user.html', form=form)

        user = User.query.filter(User.username == name).first()       # finding the first thing that 


        db.session.delete(user)
        db.session.commit()
        flash(f'User "{name}" deleted')
        return redirect ('/')


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

# reading all the products in a category/ GET FORM
@app.route('/products_for_category')
def products_for_category():
    return render_template('products_for_category.html', categories=Category.query.all())

@app.route('/nproducts_for_category', methods=['GET','POST'])
def nproducts_for_category():
    if (request.method == 'GET'):
        return render_template('nproducts_for_category.html', categories=Category.query.all())
    else:
        searched_category_id = request.form.get('category_id')
        products = Product.query.filter(Product.category_id == searched_category_id).all()
        return render_template('nproducts_for_category_results.html', products=products, categories=Category.query.all())


## ************ CREATING PRODUCTS, CATEGORIES AND POSTS******* ##

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

@app.route('/new_product', methods = ['GET', 'POST'])
def updateproduct():
   form = UpdateProduct()
   return render_template('products_for_category.html', categories=Category.query.all())


#Updating the product
@app.route('/new_product_update', methods=['PUT'])
def update(): 

    # FOR THE HTML FORM INPUT
    # form = UpdateProduct()
    # info the user wants updated (for the form)
    # name = form.name.data.strip()
    # category_id = int(form.category_id.data)
    # price = int(form.price.data)
    # product_des = form.product_des.data.strip()
    
    # FOR READING DATA THROUGH POSTMAN
    # will have to read inputs in JSON
    request_data = request.get_json() # to see if it works in postman
    
    name_to_search = None
    name_to_update = None
    category_to_update = None
    price_to_update = None
    product_des_to_update = None

    #if the user has submitted all this to be updated
    if request_data:
      if 'existing_name' in request_data:
          name_to_search = request_data['existing_name']

      if 'name_to_update' in request_data:
          name_to_update = request_data['name_to_update']

      if 'price' in request_data:
          price_to_update = int(request_data['price'])

      if 'product_des' in request_data:
          product_des_to_update = request_data['product_des']

    #find the matching product ID
    prod = db.session.query(Product).filter(Product.name == name_to_search)
    try:
        prod = prod.update(            # reassignment of updated product
            {
                "name": name_to_update,
                "price": price_to_update,
                "product_des": product_des_to_update
            }, synchronize_session = False
        )
    except Exception as exc:
        return(f"Error: {exc}")

    # db.session.add(prod)
    db.session.commit()
    flash(f'Product {name_to_search} edited')

    return(f'{prod}')
    # return redirect('/products')


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
    form = UpdateCategoryForm()

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

# reading and creating new posts in the database
@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if not form.validate_on_submit():
        return render_template('new_post.html', form=form)

    title = form.title.data.strip()
    content=form.content.data.strip()

    if Post.query.filter(Post.title == title).count():
        flash(f'Error: {title} already exists')
        return render_template('new_post.html', form=form)

    post = Post(title=title, content=content)
    db.session.add(post)
    db.session.commit()
    flash(f'New Post {title} created')
    return redirect('/')


## ********** DELETING POSTS, CATEGORIES AND PRODUCT ENTRIES FROM DB ************ ##
#Deleting existing products
@app.route('/delete_product', methods=['GET'])
def display_delete_product():
    form = RemoveProduct()
    return render_template('delete_product.html', products=Product.query.all(),form=form)

@app.route('/delete_product', methods=['POST'])
def remove_product():
    form = RemoveProduct()

    if not form.validate_on_submit():
        return render_template('delete_product.html', form=form)

    # get prod. name submitted in form
    name = request.form.get("name")
    print(name)

    category = request.form.get("category")

    # querying the database for the same product name
    if not Product.query.filter(Product.name == name).count():
        flash(f'Product "{name}" does not exist')
        return render_template('delete_product.html', form=form)

    # joining tables together
    prod_cat_join = Product.query.join(Product.category_id == Category.id)
    # filtering by user submission
    matching_prod = prod_cat_join.filter(Product.name == name, Category.name == category).one()

    #prod = Product.query.filter(Product.name == name).first()
    #print(prod)
    
    # deleting from database
    db.session.delete(matching_prod)
    db.session.commit()
    
    print("product deleted")

    flash(f'Product "{name}" deleted')
    return redirect ('/products')


# Deleting existing categories
@app.route('/delete_category', methods=['GET', 'POST'])
@login_required
def remove_category():
    form = RemoveCategory()

    if (request.method == 'GET'):
        return render_template('delete_category.html', categories=Category.query.all(),form=form)
    else:

        if not form.validate_on_submit():
            return render_template('delete_category.html', form=form)
        
        name = request.form.get("name")                                       # string that the user passes through

        if not Category.query.filter(Category.name == name).count():
            flash(f'Category "{name}" does not exist')
            return render_template('delete_category.html', form=form)

        category = Category.query.filter(Category.name == name).first()       # finding the first thing that 

        db.session.delete(category)
        db.session.commit()
        flash(f'Category "{name}" deleted')
        return redirect ('/products')

#Deleting Posts
@app.route('/delete_post', methods=['GET','POST'])
def remove_post():
    form = RemovePost()
    if (request.method == 'GET'):
        return render_template('delete_post.html', posts=Post.query.all(),form=form)

    if not form.validate_on_submit():
        return render_template('delete_post.html', form=form)
    
    title = request.form.get("title")                                       # string that the user passes through

    post = Post.query.filter(Post.title == title).first()       # finding the first thing that 

    db.session.delete(post)
    db.session.commit()
    flash(f'Post "{title}" deleted')
    return redirect ('/products')


## ******************* USER LOGOUT **************** ##

# logging out of a session
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


## ******************* SEARCH **************** ##

@app.route('/search', methods=('GET','POST'))
def search():
    if (request.method == 'GET'):
        return render_template ('search.html')
    else:
        searched_product = request.form.get('name')
        products = Product.query.filter(Product.name.ilike(f"%{searched_product}%")).all()
        return jsonify([product.as_dict() for product in products])
