from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email


class NewCategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NewProductForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    product_des = StringField('Product description', validators=[DataRequired()])
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
