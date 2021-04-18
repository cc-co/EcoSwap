from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email


class NewCategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NewProductForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    product_des = StringField('Product description', validators=[DataRequired()])
    price = IntegerField('Price (£)', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NewUserForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    email=StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords need to match')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    remember=BooleanField('Remember me')
    submit=SubmitField('Login')

class RemoveProduct(FlaskForm):
    name=StringField('Product Name', validators=[DataRequired()])
    submit = SubmitField('Delete')
    
class RemoveCategory(FlaskForm):
    name=StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Delete')

class RemoveUser(FlaskForm):
    name=StringField('User', validators=[DataRequired()])
    submit = SubmitField('Delete')


#Form for posting blog entries by users
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class RemovePost(FlaskForm):
    title=StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Delete')