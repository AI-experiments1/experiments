from flask import Blueprint, render_template, request
from app.models import Product, Category

products = Blueprint('products', __name__)


@products.route('/')
def list_products():
    category_slug = request.args.get('category', '')
    search = request.args.get('search', '').strip()
    sort = request.args.get('sort', 'default')
    page = request.args.get('page', 1, type=int)

    query = Product.query.filter_by(is_active=True)

    if category_slug:
        cat = Category.query.filter_by(slug=category_slug).first()
        if cat:
            query = query.filter_by(category_id=cat.id)

    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort == 'newest':
        query = query.order_by(Product.created_at.desc())
    else:
        query = query.order_by(Product.is_featured.desc(), Product.id)

    pagination = query.paginate(page=page, per_page=12, error_out=False)
    categories = Category.query.all()

    return render_template('products/list.html', products=pagination.items,
                           pagination=pagination, categories=categories,
                           selected_category=category_slug, search=search, sort=sort)


@products.route('/<int:product_id>')
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    related = Product.query.filter_by(category_id=product.category_id, is_active=True)\
                           .filter(Product.id != product.id).limit(4).all()
    return render_template('products/detail.html', product=product, related=related)
