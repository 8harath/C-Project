"""
Unit tests for database models
"""
import pytest
from datetime import date, timedelta
from decimal import Decimal
from models.user import User
from models.medicine import Medicine, AlternativeMedicine
from models.sale import Sale


class TestUserModel:
    """Test cases for User model"""

    def test_create_user(self, db_session):
        """Test user creation"""
        user = User(
            username='testuser',
            email='test@example.com',
            password='password123',
            role='Staff'
        )
        db_session.session.add(user)
        db_session.session.commit()

        assert user.user_id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.role == 'Staff'

    def test_password_hashing(self, db_session):
        """Test password hashing and verification"""
        user = User(
            username='testuser',
            email='test@example.com',
            password='password123',
            role='Staff'
        )
        db_session.session.add(user)
        db_session.session.commit()

        # Password should be hashed
        assert user.password_hash != 'password123'

        # Check password should work
        assert user.check_password('password123') is True
        assert user.check_password('wrongpassword') is False

    def test_is_admin(self, admin_user, staff_user):
        """Test is_admin() method"""
        assert admin_user.is_admin() is True
        assert staff_user.is_admin() is False

    def test_is_staff(self, admin_user, staff_user):
        """Test is_staff() method"""
        assert admin_user.is_staff() is False
        assert staff_user.is_staff() is True


class TestMedicineModel:
    """Test cases for Medicine model"""

    def test_create_medicine(self, db_session):
        """Test medicine creation"""
        medicine = Medicine(
            name='Test Med',
            description='Test Description',
            manufacturer='Test Mfr',
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

        assert medicine.medicine_id is not None
        assert medicine.name == 'Test Med'
        assert medicine.stock == 100

    def test_is_low_stock(self, sample_medicine, low_stock_medicine):
        """Test is_low_stock() method"""
        assert sample_medicine.is_low_stock() is False
        assert low_stock_medicine.is_low_stock() is True

    def test_is_expired(self, sample_medicine, expired_medicine):
        """Test is_expired() method"""
        assert sample_medicine.is_expired() is False
        assert expired_medicine.is_expired() is True

    def test_is_expiring_soon(self, db_session):
        """Test is_expiring_soon() method"""
        # Medicine expiring in 20 days
        medicine = Medicine(
            name='Expiring Soon',
            manufacturer='Test',
            category='Fever',
            quantity=50,
            price=Decimal('25.00'),
            expiry_date=date.today() + timedelta(days=20),
            stock=50,
            reorder_level=10,
            barcode='1234567890126'
        )
        db_session.session.add(medicine)
        db_session.session.commit()

        assert medicine.is_expiring_soon(days=30) is True
        assert medicine.is_expiring_soon(days=10) is False


class TestAlternativeMedicineModel:
    """Test cases for AlternativeMedicine model"""

    def test_create_alternative_mapping(self, db_session, sample_medicine):
        """Test creating alternative medicine mapping"""
        # Create another medicine
        alt_medicine = Medicine(
            name='Alternative Med',
            manufacturer='Test',
            category='Fever',
            quantity=50,
            price=Decimal('45.00'),
            expiry_date=date.today() + timedelta(days=365),
            stock=50,
            reorder_level=10,
            barcode='1234567890999'
        )
        db_session.session.add(alt_medicine)
        db_session.session.commit()

        # Create mapping
        mapping = AlternativeMedicine(
            primary_medicine_id=sample_medicine.medicine_id,
            alternative_medicine_id=alt_medicine.medicine_id,
            reason='Same category',
            priority=1
        )
        db_session.session.add(mapping)
        db_session.session.commit()

        assert mapping.alternative_id is not None
        assert mapping.primary_medicine_id == sample_medicine.medicine_id

    def test_get_alternatives(self, db_session, sample_medicine):
        """Test getting alternatives for a medicine"""
        # Create alternative medicines
        alt1 = Medicine(
            name='Alt Med 1',
            manufacturer='Test',
            category='Fever',
            quantity=50,
            price=Decimal('45.00'),
            expiry_date=date.today() + timedelta(days=365),
            stock=50,
            reorder_level=10,
            barcode='1234567890997'
        )
        alt2 = Medicine(
            name='Alt Med 2',
            manufacturer='Test',
            category='Fever',
            quantity=60,
            price=Decimal('40.00'),
            expiry_date=date.today() + timedelta(days=365),
            stock=60,
            reorder_level=10,
            barcode='1234567890998'
        )
        db_session.session.add_all([alt1, alt2])
        db_session.session.commit()

        # Create mappings
        mapping1 = AlternativeMedicine(
            primary_medicine_id=sample_medicine.medicine_id,
            alternative_medicine_id=alt1.medicine_id,
            priority=1
        )
        mapping2 = AlternativeMedicine(
            primary_medicine_id=sample_medicine.medicine_id,
            alternative_medicine_id=alt2.medicine_id,
            priority=2
        )
        db_session.session.add_all([mapping1, mapping2])
        db_session.session.commit()

        # Get alternatives
        alternatives = sample_medicine.get_alternatives()
        assert len(alternatives) == 2


class TestSaleModel:
    """Test cases for Sale model"""

    def test_create_sale(self, db_session, admin_user, sample_medicine):
        """Test sale creation"""
        sale = Sale(
            medicine_id=sample_medicine.medicine_id,
            user_id=admin_user.user_id,
            quantity_sold=10,
            total_price=Decimal('500.00')
        )
        db_session.session.add(sale)
        db_session.session.commit()

        assert sale.sale_id is not None
        assert sale.quantity_sold == 10
        assert sale.total_price == Decimal('500.00')

    def test_sale_relationships(self, db_session, admin_user, sample_medicine):
        """Test sale relationships with medicine and user"""
        sale = Sale(
            medicine_id=sample_medicine.medicine_id,
            user_id=admin_user.user_id,
            quantity_sold=5,
            total_price=Decimal('250.00')
        )
        db_session.session.add(sale)
        db_session.session.commit()

        # Test relationships
        assert sale.medicine.name == sample_medicine.name
        assert sale.seller.username == admin_user.username

    def test_get_season(self, db_session, admin_user, sample_medicine):
        """Test get_season() method"""
        from datetime import datetime

        sale = Sale(
            medicine_id=sample_medicine.medicine_id,
            user_id=admin_user.user_id,
            quantity_sold=5,
            total_price=Decimal('250.00')
        )
        db_session.session.add(sale)
        db_session.session.commit()

        season = sale.get_season()
        assert season in ['Winter', 'Spring', 'Summer', 'Monsoon']
