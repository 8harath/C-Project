import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User
from models.medicine import Medicine, AlternativeMedicine
from models.sale import Sale
from datetime import date, timedelta
from decimal import Decimal


@pytest.fixture(scope='session')
def app():
    """Create and configure a test Flask application"""
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create a test client for the Flask application"""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Create a test CLI runner for the Flask application"""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def db_session(app):
    """Create a database session for testing"""
    with app.app_context():
        # Clean up database
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield db
        # Cleanup
        db.session.remove()
        db.drop_all()


@pytest.fixture
def admin_user(db_session):
    """Create an admin user for testing"""
    user = User(
        username='admin_test',
        email='admin@test.com',
        password='admin123',
        role='Admin'
    )
    db_session.session.add(user)
    db_session.session.commit()
    return user


@pytest.fixture
def staff_user(db_session):
    """Create a staff user for testing"""
    user = User(
        username='staff_test',
        email='staff@test.com',
        password='staff123',
        role='Staff'
    )
    db_session.session.add(user)
    db_session.session.commit()
    return user


@pytest.fixture
def sample_medicine(db_session):
    """Create a sample medicine for testing"""
    medicine = Medicine(
        name='Test Medicine',
        description='Test Description',
        manufacturer='Test Manufacturer',
        category='Fever',
        quantity=100,
        price=Decimal('50.00'),
        expiry_date=date.today() + timedelta(days=365),
        stock=100,
        reorder_level=10,
        barcode='1234567890123'
    )
    db_session.session.add(medicine)
    db_session.session.commit()
    return medicine


@pytest.fixture
def low_stock_medicine(db_session):
    """Create a low stock medicine for testing"""
    medicine = Medicine(
        name='Low Stock Medicine',
        description='Test low stock',
        manufacturer='Test Manufacturer',
        category='Pain Relief',
        quantity=5,
        price=Decimal('25.00'),
        expiry_date=date.today() + timedelta(days=180),
        stock=5,
        reorder_level=10,
        barcode='1234567890124'
    )
    db_session.session.add(medicine)
    db_session.session.commit()
    return medicine


@pytest.fixture
def expired_medicine(db_session):
    """Create an expired medicine for testing"""
    medicine = Medicine(
        name='Expired Medicine',
        description='Test expired',
        manufacturer='Test Manufacturer',
        category='Cough',
        quantity=50,
        price=Decimal('30.00'),
        expiry_date=date.today() - timedelta(days=30),
        stock=50,
        reorder_level=10,
        barcode='1234567890125'
    )
    db_session.session.add(medicine)
    db_session.session.commit()
    return medicine


@pytest.fixture
def authenticated_admin_client(client, admin_user):
    """Create an authenticated admin client"""
    with client.session_transaction() as sess:
        sess['_user_id'] = str(admin_user.user_id)
    return client


@pytest.fixture
def authenticated_staff_client(client, staff_user):
    """Create an authenticated staff client"""
    with client.session_transaction() as sess:
        sess['_user_id'] = str(staff_user.user_id)
    return client
