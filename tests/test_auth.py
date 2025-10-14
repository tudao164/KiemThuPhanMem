import pytest
from datetime import datetime, timedelta

class TestAuth:
    """UC-01, UC-02, UC-08: Authentication tests"""
    
    def test_register_success(self, client):
        """UC-01: Test successful registration"""
        user_data = {
            "email": "newuser@example.com",
            "name": "New User",
            "password": "password123"
        }
        response = client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["name"] == user_data["name"]
        assert "id" in data
        assert "hashed_password" not in data  # Password should not be returned
    
    def test_register_duplicate_email(self, client, test_user):
        """UC-01: Test registration with duplicate email returns 409"""
        user_data = {
            "email": test_user["email"],
            "name": "Another User",
            "password": "password123"
        }
        response = client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == 409
        assert "already registered" in response.json()["detail"].lower()
    
    def test_register_invalid_data(self, client):
        """UC-01: Test registration with invalid data returns 400"""
        user_data = {
            "email": "invalid-email",  # Invalid email format
            "name": "Test User",
            "password": "12345"  # Too short
        }
        response = client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_login_success(self, client, test_user):
        """UC-02: Test successful login"""
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self, client, test_user):
        """UC-02: Test login with wrong password returns 401"""
        login_data = {
            "email": test_user["email"],
            "password": "wrongpassword"
        }
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self, client):
        """UC-02: Test login with non-existent user returns 401"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "password123"
        }
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 401
    
    def test_logout_success(self, client, auth_headers):
        """UC-08: Test successful logout"""
        response = client.post("/api/auth/logout", headers=auth_headers)
        
        assert response.status_code == 200
        assert "logged out" in response.json()["message"].lower()
    
    def test_logout_without_token(self, client):
        """UC-08: Test logout without token returns 401"""
        response = client.post("/api/auth/logout")
        
        assert response.status_code == 403  # No credentials provided
    
    def test_token_blacklist(self, client, auth_headers):
        """UC-08: Test that blacklisted token cannot be used"""
        # Logout (blacklist token)
        response = client.post("/api/auth/logout", headers=auth_headers)
        assert response.status_code == 200
        
        # Try to use the same token
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == 401
    
    def test_get_current_user(self, client, auth_headers):
        """Test getting current user info"""
        response = client.get("/api/auth/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert "name" in data
