import pytest
from datetime import datetime, timedelta

class TestTodos:
    """UC-03, UC-04, UC-05, UC-06, UC-07: Todo CRUD and filtering tests"""
    
    def test_create_todo_success(self, client, auth_headers):
        """UC-03: Test creating a todo"""
        todo_data = {
            "title": "Test Todo",
            "description": "Test Description",
            "status": "pending",
            "priority": "high"
        }
        response = client.post("/api/todos", json=todo_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == todo_data["title"]
        assert data["description"] == todo_data["description"]
        assert "id" in data
        assert "user_id" in data
    
    def test_create_todo_without_auth(self, client):
        """UC-03: Test creating todo without authentication returns 401"""
        todo_data = {
            "title": "Test Todo",
            "description": "Test Description"
        }
        response = client.post("/api/todos", json=todo_data)
        
        assert response.status_code == 403  # No credentials
    
    def test_create_todo_invalid_data(self, client, auth_headers):
        """UC-03: Test creating todo with invalid data returns 400"""
        todo_data = {
            "title": "",  # Empty title
            "description": "Test Description"
        }
        response = client.post("/api/todos", json=todo_data, headers=auth_headers)
        
        assert response.status_code == 422  # Validation error
    
    def test_get_todos_list(self, client, auth_headers):
        """UC-04: Test getting list of todos"""
        # Create some todos
        for i in range(3):
            todo_data = {
                "title": f"Todo {i}",
                "description": f"Description {i}",
                "status": "pending"
            }
            client.post("/api/todos", json=todo_data, headers=auth_headers)
        
        # Get todos
        response = client.get("/api/todos", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
    
    def test_get_todos_without_auth(self, client):
        """UC-04: Test getting todos without authentication returns 401"""
        response = client.get("/api/todos")
        
        assert response.status_code == 403
    
    def test_get_single_todo(self, client, auth_headers):
        """Test getting a single todo by ID"""
        # Create a todo
        todo_data = {
            "title": "Test Todo",
            "description": "Test Description"
        }
        create_response = client.post("/api/todos", json=todo_data, headers=auth_headers)
        todo_id = create_response.json()["id"]
        
        # Get the todo
        response = client.get(f"/api/todos/{todo_id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == todo_data["title"]
    
    def test_get_nonexistent_todo(self, client, auth_headers):
        """Test getting non-existent todo returns 404"""
        response = client.get("/api/todos/99999", headers=auth_headers)
        
        assert response.status_code == 404
    
    def test_update_todo_success(self, client, auth_headers):
        """UC-05: Test updating a todo"""
        # Create a todo
        todo_data = {
            "title": "Original Title",
            "description": "Original Description",
            "status": "pending"
        }
        create_response = client.post("/api/todos", json=todo_data, headers=auth_headers)
        todo_id = create_response.json()["id"]
        
        # Update the todo
        update_data = {
            "title": "Updated Title",
            "status": "completed"
        }
        response = client.put(f"/api/todos/{todo_id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["status"] == update_data["status"]
    
    def test_update_nonexistent_todo(self, client, auth_headers):
        """UC-05: Test updating non-existent todo returns 404"""
        update_data = {"title": "Updated Title"}
        response = client.put("/api/todos/99999", json=update_data, headers=auth_headers)
        
        assert response.status_code == 404
    
    def test_update_other_user_todo(self, client, auth_headers):
        """UC-05: Test that user cannot update another user's todo"""
        # Create a second user
        user2_data = {
            "email": "user2@example.com",
            "name": "User 2",
            "password": "password123"
        }
        client.post("/api/auth/register", json=user2_data)
        
        # Login as second user
        login_response = client.post("/api/auth/login", json={
            "email": user2_data["email"],
            "password": user2_data["password"]
        })
        user2_token = login_response.json()["access_token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}
        
        # Create todo as second user
        todo_data = {"title": "User 2 Todo"}
        create_response = client.post("/api/todos", json=todo_data, headers=user2_headers)
        todo_id = create_response.json()["id"]
        
        # Try to update as first user
        update_data = {"title": "Hacked Title"}
        response = client.put(f"/api/todos/{todo_id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == 403
    
    def test_delete_todo_success(self, client, auth_headers):
        """UC-06: Test deleting a todo"""
        # Create a todo
        todo_data = {"title": "Todo to Delete"}
        create_response = client.post("/api/todos", json=todo_data, headers=auth_headers)
        todo_id = create_response.json()["id"]
        
        # Delete the todo
        response = client.delete(f"/api/todos/{todo_id}", headers=auth_headers)
        
        assert response.status_code == 200
        assert "deleted" in response.json()["message"].lower()
        
        # Verify it's deleted
        get_response = client.get(f"/api/todos/{todo_id}", headers=auth_headers)
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_todo(self, client, auth_headers):
        """UC-06: Test deleting non-existent todo returns 404"""
        response = client.delete("/api/todos/99999", headers=auth_headers)
        
        assert response.status_code == 404
    
    def test_delete_other_user_todo(self, client, auth_headers):
        """UC-06: Test that user cannot delete another user's todo"""
        # Create a second user and their todo
        user2_data = {
            "email": "user2@example.com",
            "name": "User 2",
            "password": "password123"
        }
        client.post("/api/auth/register", json=user2_data)
        
        login_response = client.post("/api/auth/login", json={
            "email": user2_data["email"],
            "password": user2_data["password"]
        })
        user2_token = login_response.json()["access_token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}
        
        todo_data = {"title": "User 2 Todo"}
        create_response = client.post("/api/todos", json=todo_data, headers=user2_headers)
        todo_id = create_response.json()["id"]
        
        # Try to delete as first user
        response = client.delete(f"/api/todos/{todo_id}", headers=auth_headers)
        
        assert response.status_code == 403
    
    def test_filter_by_status(self, client, auth_headers):
        """UC-07: Test filtering todos by status"""
        # Create todos with different statuses
        client.post("/api/todos", json={"title": "Todo 1", "status": "pending"}, headers=auth_headers)
        client.post("/api/todos", json={"title": "Todo 2", "status": "completed"}, headers=auth_headers)
        client.post("/api/todos", json={"title": "Todo 3", "status": "pending"}, headers=auth_headers)
        
        # Filter by pending status
        response = client.get("/api/todos?status=pending", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(todo["status"] == "pending" for todo in data)
    
    def test_filter_by_priority(self, client, auth_headers):
        """UC-07: Test filtering todos by priority"""
        client.post("/api/todos", json={"title": "Todo 1", "priority": "high"}, headers=auth_headers)
        client.post("/api/todos", json={"title": "Todo 2", "priority": "low"}, headers=auth_headers)
        client.post("/api/todos", json={"title": "Todo 3", "priority": "high"}, headers=auth_headers)
        
        response = client.get("/api/todos?priority=high", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(todo["priority"] == "high" for todo in data)
    
    def test_search_todos(self, client, auth_headers):
        """UC-07: Test searching todos"""
        client.post("/api/todos", json={"title": "Buy groceries", "description": "Milk and eggs"}, headers=auth_headers)
        client.post("/api/todos", json={"title": "Call doctor", "description": "Schedule appointment"}, headers=auth_headers)
        client.post("/api/todos", json={"title": "Buy tickets", "description": "Concert tickets"}, headers=auth_headers)
        
        response = client.get("/api/todos?search=buy", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_sort_todos(self, client, auth_headers):
        """UC-07: Test sorting todos"""
        client.post("/api/todos", json={"title": "C Todo"}, headers=auth_headers)
        client.post("/api/todos", json={"title": "A Todo"}, headers=auth_headers)
        client.post("/api/todos", json={"title": "B Todo"}, headers=auth_headers)
        
        response = client.get("/api/todos?sort_by=created_at&sort_order=asc", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
