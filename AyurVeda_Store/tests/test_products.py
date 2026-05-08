from app.models import Product


def test_product_list_loads(client):
    assert client.get('/products/').status_code == 200


def test_product_list_shows_active_products(client):
    resp = client.get('/products/')
    assert b'Ashwagandha' in resp.data
    assert b'Basmati Rice' in resp.data


def test_product_list_hides_inactive(client):
    resp = client.get('/products/')
    assert b'Inactive Item' not in resp.data


def test_search_returns_matching_product(client):
    resp = client.get('/products/?search=ashwagandha')
    assert resp.status_code == 200
    assert b'Ashwagandha' in resp.data
    assert b'Basmati' not in resp.data


def test_search_no_results(client):
    resp = client.get('/products/?search=xyznotexist99')
    assert resp.status_code == 200


def test_filter_by_category(client):
    resp = client.get('/products/?category=ayurvedic')
    assert resp.status_code == 200
    assert b'Ashwagandha' in resp.data
    assert b'Basmati' not in resp.data


def test_filter_agricultural_category(client):
    resp = client.get('/products/?category=agricultural')
    assert b'Basmati' in resp.data
    assert b'Ashwagandha' not in resp.data


def test_sort_price_asc(client):
    assert client.get('/products/?sort=price_asc').status_code == 200


def test_sort_price_desc(client):
    assert client.get('/products/?sort=price_desc').status_code == 200


def test_product_detail_valid(app, client):
    with app.app_context():
        p = Product.query.filter_by(name='Ashwagandha Powder').first()
        pid = p.id
    resp = client.get(f'/products/{pid}')
    assert resp.status_code == 200
    assert b'Ashwagandha' in resp.data


def test_product_detail_not_found(client):
    assert client.get('/products/99999').status_code == 404
