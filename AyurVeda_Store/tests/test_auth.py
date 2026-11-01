def test_register_page_loads(client):
    assert client.get('/auth/register').status_code == 200


def test_register_success(client):
    resp = client.post('/auth/register', data={
        'name': 'New User',
        'email': 'new@test.com',
        'phone': '9876543299',
        'password': 'newpass123',
        'confirm': 'newpass123',
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Account created' in resp.data


def test_register_duplicate_email(client):
    resp = client.post('/auth/register', data={
        'name': 'Dup',
        'email': 'user@test.com',
        'password': 'pass1234',
        'confirm': 'pass1234',
    }, follow_redirects=True)
    assert b'already registered' in resp.data


def test_login_page_loads(client):
    assert client.get('/auth/login').status_code == 200


def test_login_success(client):
    resp = client.post('/auth/login', data={
        'email': 'user@test.com',
        'password': 'testpass123',
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Welcome back' in resp.data


def test_login_wrong_password(client):
    resp = client.post('/auth/login', data={
        'email': 'user@test.com',
        'password': 'wrongpass',
    }, follow_redirects=True)
    assert b'Invalid email or password' in resp.data


def test_login_unknown_email(client):
    resp = client.post('/auth/login', data={
        'email': 'nobody@test.com',
        'password': 'pass',
    }, follow_redirects=True)
    assert b'Invalid email or password' in resp.data


def test_profile_redirects_when_unauthenticated(client):
    resp = client.get('/auth/profile')
    assert resp.status_code == 302
    assert b'/auth/login' in resp.headers['Location'].encode()


def test_profile_loads_when_logged_in(auth_client):
    assert auth_client.get('/auth/profile').status_code == 200


def test_logout(auth_client):
    resp = auth_client.get('/auth/logout', follow_redirects=True)
    assert b'logged out' in resp.data


def test_login_rejects_external_next_redirect(client):
    resp = client.post('/auth/login?next=https://evil.example.com/',
                       data={'email': 'user@test.com', 'password': 'testpass123'})
    assert resp.status_code == 302
    assert 'evil.example.com' not in resp.headers['Location']


def test_login_rejects_protocol_relative_next_redirect(client):
    resp = client.post('/auth/login?next=//evil.example.com/',
                       data={'email': 'user@test.com', 'password': 'testpass123'})
    assert resp.status_code == 302
    assert 'evil.example.com' not in resp.headers['Location']


def test_login_allows_relative_next_redirect(client):
    resp = client.post('/auth/login?next=/cart/',
                       data={'email': 'user@test.com', 'password': 'testpass123'})
    assert resp.status_code == 302
    assert resp.headers['Location'].endswith('/cart/')


def test_login_email_case_insensitive(client):
    resp = client.post('/auth/login',
                       data={'email': 'USER@test.com', 'password': 'testpass123'})
    assert resp.status_code == 302
