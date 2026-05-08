from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import CartItem, Product, Order, OrderItem
from app.forms import CheckoutForm

cart = Blueprint('cart', __name__)


@cart.route('/')
@login_required
def view_cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.subtotal for item in items)
    return render_template('cart/cart.html', items=items, total=total)


@cart.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        item.quantity += quantity
    else:
        item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(item)
    db.session.commit()
    flash(f'"{product.name}" added to cart!', 'success')
    return redirect(request.referrer or url_for('products.list_products'))


@cart.route('/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('cart.view_cart'))
    quantity = int(request.form.get('quantity', 1))
    if quantity <= 0:
        db.session.delete(item)
    else:
        item.quantity = quantity
    db.session.commit()
    return redirect(url_for('cart.view_cart'))


@cart.route('/remove/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('cart.view_cart'))
    db.session.delete(item)
    db.session.commit()
    flash('Item removed from cart.', 'info')
    return redirect(url_for('cart.view_cart'))


@cart.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('cart.view_cart'))

    form = CheckoutForm()
    if request.method == 'GET':
        form.name.data = current_user.name
        form.phone.data = current_user.phone
        form.address.data = current_user.address

    total = sum(item.subtotal for item in items)

    if form.validate_on_submit():
        order = Order(
            user_id=current_user.id,
            total=total,
            shipping_address=form.address.data,
            phone=form.phone.data,
            payment_method=form.payment_method.data
        )
        db.session.add(order)
        db.session.flush()

        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.session.add(order_item)
            item.product.stock = max(0, item.product.stock - item.quantity)
            db.session.delete(item)

        db.session.commit()
        flash(f'Order #{order.id} placed successfully! Thank you for shopping with us.', 'success')
        return redirect(url_for('cart.order_success', order_id=order.id))

    return render_template('cart/checkout.html', form=form, items=items, total=total)


@cart.route('/order-success/<int:order_id>')
@login_required
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        return redirect(url_for('main.index'))
    return render_template('cart/order_success.html', order=order)


@cart.route('/my-orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('cart/my_orders.html', orders=orders)
