import pytest
from app.models import User, Product, CartItem, OrderItem


def test_user_password_correct(app):
    with app.app_context():
        u = User(name='Alice', email='alice@x.com')
        u.set_password('mysecret')
        assert u.check_password('mysecret')


def test_user_password_wrong(app):
    with app.app_context():
        u = User(name='Bob', email='bob@x.com')
        u.set_password('correct')
        assert not u.check_password('wrong')
        assert not u.check_password('')


def test_product_discount_with_original_price():
    p = Product(price=300, original_price=400)
    assert p.discount_percent == 25


def test_product_discount_no_original_price():
    p = Product(price=300)
    assert p.discount_percent == 0


def test_product_discount_original_not_higher():
    # original_price <= price means no discount
    p = Product(price=300, original_price=200)
    assert p.discount_percent == 0


def test_product_discount_equal_prices():
    p = Product(price=300, original_price=300)
    assert p.discount_percent == 0


def test_cart_item_subtotal():
    p = Product(price=249.0)
    item = CartItem(product=p, quantity=4)
    assert item.subtotal == pytest.approx(996.0)


def test_order_item_subtotal():
    item = OrderItem(price=150.0, quantity=3)
    assert item.subtotal == pytest.approx(450.0)
