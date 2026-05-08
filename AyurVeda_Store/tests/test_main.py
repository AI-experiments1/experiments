def test_index_loads(client):
    assert client.get('/').status_code == 200


def test_index_shows_featured_products(client):
    resp = client.get('/')
    assert b'Ashwagandha' in resp.data


def test_about_loads(client):
    assert client.get('/about').status_code == 200


def test_contact_loads(client):
    assert client.get('/contact').status_code == 200
