"""
Unit tests for Flask routes
"""
import pytest
from flask import url_for


class TestAuthRoutes:
    """Test cases for authentication routes"""

    def test_login_page_loads(self, client):
        """Test login page loads correctly"""
        response = client.get('/auth/login')
        assert response.status_code == 200

    def test_register_page_loads(self, client):
        """Test register page loads correctly"""
        response = client.get('/auth/register')
        assert response.status_code == 200


class TestMedicineRoutes:
    """Test cases for medicine routes"""

    def test_medicine_list_requires_auth(self, client):
        """Test medicine list requires authentication"""
        response = client.get('/medicines/')
        # Should redirect to login
        assert response.status_code == 302
        assert '/auth/login' in response.location


class TestSalesRoutes:
    """Test cases for sales routes"""

    def test_sell_page_requires_auth(self, client):
        """Test sell page requires authentication"""
        response = client.get('/sales/sell')
        # Should redirect to login
        assert response.status_code == 302

    def test_scan_page_requires_auth(self, client):
        """Test scan page requires authentication"""
        response = client.get('/sales/scan')
        # Should redirect to login
        assert response.status_code == 302


class TestAdminRoutes:
    """Test cases for admin routes"""

    def test_admin_dashboard_requires_auth(self, client):
        """Test admin dashboard requires authentication"""
        response = client.get('/admin/dashboard')
        # Should redirect to login
        assert response.status_code == 302

    def test_predictive_insights_requires_auth(self, client):
        """Test predictive insights requires authentication"""
        response = client.get('/admin/predictive-insights')
        # Should redirect to login
        assert response.status_code == 302
