from flask import Blueprint, render_template
from app.models import Product, Category

main = Blueprint('main', __name__)


@main.route('/')
def index():
    featured = Product.query.filter_by(is_featured=True, is_active=True).limit(8).all()
    categories = Category.query.all()
    return render_template('index.html', featured=featured, categories=categories)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/contact')
def contact():
    return render_template('contact.html')
