from app import db
from app.models import Product, CartItem, User


def _product_id(app, name):
    with app.app_context():
        return Product.query.filter_by(name=name).first().id


def test_cart_redirects_when_unauthenticated(client):
    resp = client.get('/cart/')
    assert resp.status_code == 302
    assert b'/auth/login' in resp.headers['Location'].encode()


def test_cart_empty(auth_client):
    resp = auth_client.get('/cart/')
    assert resp.status_code == 200
    assert b'empty' in resp.data.lower()


def test_add_to_cart(app, auth_client):
    pid = _product_id(app, 'Ashwagandha Powder')
    resp = auth_client.post(f'/cart/add/{pid}', data={'quantity': '2'},
                            follow_redirects=True)
    assert resp.status_code == 200
    assert b'added to cart' in resp.data.lower()


def test_cart_shows_added_item(app, auth_client):
    pid = _product_id(app, 'Ashwagandha Powder')
    auth_client.post(f'/cart/add/{pid}', data={'quantity': '1'})
    resp = auth_client.get('/cart/')
    assert b'Ashwagandha' in resp.data


def test_remove_from_cart(app, auth_client):
    pid = _product_id(app, 'Basmati Rice')
    auth_client.post(f'/cart/add/{pid}', data={'quantity': '1'})

    with app.app_context():
        user = User.query.filter_by(email='user@test.com').first()
        item = CartItem.query.filter_by(user_id=user.id, product_id=pid).first()
        item_id = item.id

    resp = auth_client.get(f'/cart/remove/{item_id}', follow_redirects=True)
    assert b'removed' in resp.data.lower()


def test_checkout_empty_cart_redirects(auth_client):
    resp = auth_client.get('/cart/checkout', follow_redirects=True)
    assert b'empty' in resp.data.lower()


def test_checkout_places_order(app, auth_client):
    pid = _product_id(app, 'Ashwagandha Powder')
    auth_client.post(f'/cart/add/{pid}', data={'quantity': '1'})
    resp = auth_client.post('/cart/checkout', data={
        'name': 'Test User',
        'phone': '9876543210',
        'address': '123 Test Street, Pune - 411001',
        'payment_method': 'COD',
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'successfully' in resp.data.lower()


def test_my_orders_redirects_when_unauthenticated(client):
    resp = client.get('/cart/my-orders')
    assert resp.status_code == 302


def test_my_orders_loads(auth_client):
    assert auth_client.get('/cart/my-orders').status_code == 200


def test_my_orders_shows_past_order(app, auth_client):
    pid = _product_id(app, 'Basmati Rice')
    auth_client.post(f'/cart/add/{pid}', data={'quantity': '1'})
    auth_client.post('/cart/checkout', data={
        'name': 'Test User',
        'phone': '9876543210',
        'address': '123 Test Street, Pune - 411001',
        'payment_method': 'COD',
    })
    resp = auth_client.get('/cart/my-orders')
    assert b'Basmati' in resp.data


def test_add_to_cart_invalid_quantity_does_not_crash(app, auth_client):
    pid = _product_id(app, 'Ashwagandha Powder')
    resp = auth_client.post(f'/cart/add/{pid}', data={'quantity': 'abc'}, follow_redirects=True)
    assert resp.status_code == 200
    assert b'valid quantity' in resp.data.lower()


def test_add_to_cart_rejects_negative_quantity(app, auth_client):
    pid = _product_id(app, 'Ashwagandha Powder')
    auth_client.post(f'/cart/add/{pid}', data={'quantity': '-5'})
    with app.app_context():
        assert CartItem.query.count() == 0


def test_add_to_cart_respects_stock(app, auth_client):
    pid = _product_id(app, 'Ashwagandha Powder')  # seeded with stock=50
    resp = auth_client.post(f'/cart/add/{pid}', data={'quantity': '51'}, follow_redirects=True)
    assert b'in stock' in resp.data.lower()
    with app.app_context():
        assert CartItem.query.count() == 0


def test_add_inactive_product_to_cart_rejected(app, auth_client):
    pid = _product_id(app, 'Inactive Item')
    auth_client.post(f'/cart/add/{pid}', data={'quantity': '1'})
    with app.app_context():
        assert CartItem.query.count() == 0


def test_update_cart_invalid_quantity_does_not_crash(app, auth_client):
    pid = _product_id(app, 'Ashwagandha Powder')
    auth_client.post(f'/cart/add/{pid}', data={'quantity': '1'})
    with app.app_context():
        item_id = CartItem.query.first().id
    resp = auth_client.post(f'/cart/update/{item_id}', data={'quantity': 'x'}, follow_redirects=True)
    assert resp.status_code == 200


def test_checkout_decrements_stock(app, auth_client):
    pid = _product_id(app, 'Ashwagandha Powder')
    auth_client.post(f'/cart/add/{pid}', data={'quantity': '3'})
    auth_client.post('/cart/checkout', data={
        'name': 'Test User', 'phone': '9876543210',
        'address': '123 Test Street, Pune - 411001', 'payment_method': 'COD',
    })
    with app.app_context():
        assert db.session.get(Product, pid).stock == 47
