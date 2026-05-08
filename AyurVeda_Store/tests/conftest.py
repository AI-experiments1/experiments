import pytest
from sqlalchemy.pool import StaticPool
from app import create_app, db as _db
from app.models import Category, Product, User

TEST_CONFIG = {
    'TESTING': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    'SQLALCHEMY_ENGINE_OPTIONS': {
        'connect_args': {'check_same_thread': False},
        'poolclass': StaticPool,
    },
    'WTF_CSRF_ENABLED': False,
    'SECRET_KEY': 'test-secret-key',
}


@pytest.fixture()
def app():
    _app = create_app(TEST_CONFIG)
    with _app.app_context():
        _seed()
    yield _app


def _seed():
    cat_ayur = Category(name='Ayurvedic Products', slug='ayurvedic',
                        description='Ayurvedic herbs and medicines')
    cat_agri = Category(name='Agricultural Products', slug='agricultural',
                        description='Farm fresh produce')
    _db.session.add_all([cat_ayur, cat_agri])
    _db.session.flush()

    _db.session.add_all([
        Product(
            name='Ashwagandha Powder',
            description='Pure organic ashwagandha root powder for stress relief and immunity boost.',
            price=299, original_price=399, stock=50,
            category_id=cat_ayur.id, unit='250g', is_featured=True, is_active=True,
        ),
        Product(
            name='Basmati Rice',
            description='Premium long-grain aged basmati rice, naturally grown without pesticides.',
            price=599, stock=100,
            category_id=cat_agri.id, unit='5kg', is_featured=True, is_active=True,
        ),
        Product(
            name='Inactive Item',
            description='This product is hidden from customers and should not appear in listings.',
            price=100, stock=10,
            category_id=cat_ayur.id, unit='1pc', is_active=False,
        ),
    ])

    user = User(name='Test User', email='user@test.com',
                phone='9876543210', address='123 Test Street, Pune - 411001')
    user.set_password('testpass123')

    admin = User(name='Admin User', email='admin@test.com', is_admin=True,
                 phone='9876543211', address='456 Admin Road, Pune - 411001')
    admin.set_password('adminpass123')

    _db.session.add_all([user, admin])
    _db.session.commit()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_client(app):
    c = app.test_client()
    c.post('/auth/login', data={'email': 'user@test.com', 'password': 'testpass123'})
    return c


@pytest.fixture()
def admin_client(app):
    c = app.test_client()
    c.post('/auth/login', data={'email': 'admin@test.com', 'password': 'adminpass123'})
    return c
