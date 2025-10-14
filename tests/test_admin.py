import pytest

class TestAdmin:
    """UC-09, UC-10: Admin functionality tests"""
    
    def test_get_all_users_as_admin(self, client, admin_headers, test_user):
        """UC-09: Test admin can view all users"""
        response = client.get("/api/admin/users", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2  # At least admin and test_user
    
    def test_get_all_users_as_regular_user(self, client, auth_headers):
        """UC-09: Test regular user cannot view all users"""
        response = client.get("/api/admin/users", headers=auth_headers)
        
        assert response.status_code == 403
    
    def test_block_user_as_admin(self, client, admin_headers, test_user):
        """UC-09: Test admin can block user"""
        # Get user ID
        users_response = client.get("/api/admin/users", headers=admin_headers)
        users = users_response.json()
        user_to_block = next(u for u in users if u["email"] == test_user["email"])
        
        # Block user
        response = client.put(f"/api/admin/users/{user_to_block['id']}/block", headers=admin_headers)
        
        assert response.status_code == 200
        assert "blocked" in response.json()["message"].lower()
    
    def test_unblock_user_as_admin(self, client, admin_headers, test_user):
        """UC-09: Test admin can unblock user"""
        # Get user ID
        users_response = client.get("/api/admin/users", headers=admin_headers)
        users = users_response.json()
        user_to_unblock = next(u for u in users if u["email"] == test_user["email"])
        
        # Block then unblock
        client.put(f"/api/admin/users/{user_to_unblock['id']}/block", headers=admin_headers)
        response = client.put(f"/api/admin/users/{user_to_unblock['id']}/unblock", headers=admin_headers)
        
        assert response.status_code == 200
        assert "unblocked" in response.json()["message"].lower()
    
    def test_delete_user_as_admin(self, client, admin_headers):
        """UC-09: Test admin can delete user"""
        # Create a user to delete
        user_data = {
            "email": "todelete@example.com",
            "name": "To Delete",
            "password": "password123"
        }
        client.post("/api/auth/register", json=user_data)
        
        # Get user ID
        users_response = client.get("/api/admin/users", headers=admin_headers)
        users = users_response.json()
        user_to_delete = next(u for u in users if u["email"] == user_data["email"])
        
        # Delete user
        response = client.delete(f"/api/admin/users/{user_to_delete['id']}", headers=admin_headers)
        
        assert response.status_code == 200
        assert "deleted" in response.json()["message"].lower()
    
    def test_cannot_delete_admin(self, client, admin_headers):
        """UC-09: Test admin cannot delete another admin"""
        # Get admin user ID
        users_response = client.get("/api/admin/users", headers=admin_headers)
        users = users_response.json()
        admin_user = next(u for u in users if u["role"] == "admin")
        
        # Try to delete admin
        response = client.delete(f"/api/admin/users/{admin_user['id']}", headers=admin_headers)
        
        assert response.status_code == 403
    
    def test_get_system_stats(self, client, admin_headers, test_user):
        """UC-10: Test getting system statistics"""
        # Create some todos
        login_response = client.post("/api/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        user_token = login_response.json()["access_token"]
        user_headers = {"Authorization": f"Bearer {user_token}"}
        
        client.post("/api/todos", json={"title": "Todo 1", "status": "pending"}, headers=user_headers)
        client.post("/api/todos", json={"title": "Todo 2", "status": "completed"}, headers=user_headers)
        
        # Get stats
        response = client.get("/api/admin/stats", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "total_users" in data
        assert "active_users" in data
        assert "total_todos" in data
        assert "completed_todos" in data
        assert "pending_todos" in data
        assert data["total_users"] >= 2
        assert data["total_todos"] >= 2
        assert data["completed_todos"] >= 1
        assert data["pending_todos"] >= 1
    
    def test_get_stats_as_regular_user(self, client, auth_headers):
        """UC-10: Test regular user cannot access stats"""
        response = client.get("/api/admin/stats", headers=auth_headers)
        
        assert response.status_code == 403
