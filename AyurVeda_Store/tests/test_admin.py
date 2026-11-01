from app import db
from app.models import Category, Product


def test_dashboard_redirects_when_unauthenticated(client):
    assert client.get('/admin/').status_code == 302


def test_dashboard_blocks_regular_user(auth_client):
    resp = auth_client.get('/admin/', follow_redirects=True)
    assert b'Admin access required' in resp.data


def test_dashboard_accessible_to_admin(admin_client):
    assert admin_client.get('/admin/').status_code == 200


def test_dashboard_shows_stats(admin_client):
    resp = admin_client.get('/admin/')
    assert b'Products' in resp.data
    assert b'Orders' in resp.data


def test_admin_products_list(admin_client):
    resp = admin_client.get('/admin/products')
    assert resp.status_code == 200
    assert b'Ashwagandha' in resp.data


def test_admin_add_product_get(admin_client):
    assert admin_client.get('/admin/products/add').status_code == 200


def test_admin_add_product_post(app, admin_client):
    with app.app_context():
        cat_id = Category.query.first().id

    resp = admin_client.post('/admin/products/add', data={
        'name': 'New Test Product',
        'description': 'A description for the new product that is long enough.',
        'price': '199',
        'original_price': '249',
        'stock': '30',
        'unit': '100g',
        'category_id': str(cat_id),
        'image_url': '',
        'is_active': 'y',
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'added successfully' in resp.data


def test_admin_edit_product(app, admin_client):
    with app.app_context():
        p = Product.query.filter_by(name='Basmati Rice').first()
        cat_id = p.category_id
        pid = p.id

    resp = admin_client.post(f'/admin/products/edit/{pid}', data={
        'name': 'Updated Basmati Rice',
        'description': 'Updated description for basmati rice product, grown organically.',
        'price': '649',
        'stock': '90',
        'unit': '5kg',
        'category_id': str(cat_id),
        'image_url': '',
        'is_active': 'y',
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'updated successfully' in resp.data


def test_admin_delete_product(app, admin_client):
    with app.app_context():
        cat_id = Category.query.first().id
        p = Product(
            name='To Delete', description='Will be deleted.', price=50,
            stock=5, category_id=cat_id, unit='1pc',
        )
        db.session.add(p)
        db.session.commit()
        pid = p.id

    resp = admin_client.post(f'/admin/products/delete/{pid}',
                             follow_redirects=True)
    assert resp.status_code == 200
    assert b'deleted' in resp.data.lower()


def test_admin_orders_list(admin_client):
    assert admin_client.get('/admin/orders').status_code == 200


def test_admin_update_order_status(app, auth_client, admin_client):
    from app.models import Product as P
    with app.app_context():
        p = P.query.filter_by(name='Ashwagandha Powder').first()
        pid = p.id

    # User places an order
    auth_client.post(f'/cart/add/{pid}', data={'quantity': '1'})
    auth_client.post('/cart/checkout', data={
        'name': 'Test User', 'phone': '9876543210',
        'address': '123 Test Street, Pune - 411001', 'payment_method': 'COD',
    })

    with app.app_context():
        from app.models import Order
        order = Order.query.first()
        oid = order.id

    resp = admin_client.post(f'/admin/orders/{oid}/status',
                             data={'status': 'Confirmed'}, follow_redirects=True)
    assert resp.status_code == 200
    assert b'status updated' in resp.data.lower()


def _place_order(app, auth_client, qty='2'):
    from app.models import Product as P, Order
    with app.app_context():
        pid = P.query.filter_by(name='Ashwagandha Powder').first().id
    auth_client.post(f'/cart/add/{pid}', data={'quantity': qty})
    auth_client.post('/cart/checkout', data={
        'name': 'Test User', 'phone': '9876543210',
        'address': '123 Test Street, Pune - 411001', 'payment_method': 'COD',
    })
    with app.app_context():
        return pid, Order.query.first().id


def test_admin_rejects_invalid_order_status(app, auth_client, admin_client):
    from app import db
    from app.models import Order
    _, oid = _place_order(app, auth_client)
    resp = admin_client.post(f'/admin/orders/{oid}/status',
                             data={'status': 'Hacked'}, follow_redirects=True)
    assert b'invalid order status' in resp.data.lower()
    with app.app_context():
        assert db.session.get(Order, oid).status == 'Pending'


def test_admin_cancel_order_restores_stock(app, auth_client, admin_client):
    from app import db
    from app.models import Product as P
    pid, oid = _place_order(app, auth_client, qty='2')
    with app.app_context():
        assert db.session.get(P, pid).stock == 48
    admin_client.post(f'/admin/orders/{oid}/status', data={'status': 'Cancelled'})
    with app.app_context():
        assert db.session.get(P, pid).stock == 50


def test_admin_delete_product_with_orders_deactivates(app, auth_client, admin_client):
    from app import db
    from app.models import Product as P
    pid, _ = _place_order(app, auth_client)
    resp = admin_client.post(f'/admin/products/delete/{pid}', follow_redirects=True)
    assert resp.status_code == 200
    with app.app_context():
        p = db.session.get(P, pid)
        assert p is not None and p.is_active is False


def test_admin_add_product_with_zero_stock(app, admin_client):
    from app.models import Category, Product as P
    with app.app_context():
        cid = Category.query.first().id
    admin_client.post('/admin/products/add', data={
        'name': 'Zero Stock Item', 'description': 'Out of stock for now.',
        'price': '100', 'stock': '0', 'unit': '1pc', 'category_id': str(cid),
        'is_active': 'y',
    })
    with app.app_context():
        assert P.query.filter_by(name='Zero Stock Item').first() is not None
