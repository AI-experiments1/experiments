from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional


class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(2, 120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(6)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CheckoutForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(10, 15)])
    address = TextAreaField('Delivery Address', validators=[DataRequired(), Length(10)])
    payment_method = SelectField('Payment Method', choices=[('COD', 'Cash on Delivery'), ('UPI', 'UPI Payment'), ('Card', 'Debit/Credit Card')])
    submit = SubmitField('Place Order')


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(2, 200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price (₹)', validators=[DataRequired(), NumberRange(min=1)])
    original_price = FloatField('Original Price (₹)', validators=[Optional(), NumberRange(min=1)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    unit = StringField('Unit (e.g. 250g, 1L)', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[Optional()])
    is_featured = BooleanField('Featured Product')
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Product')
