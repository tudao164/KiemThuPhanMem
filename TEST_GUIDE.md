# Hướng dẫn Test API với Postman

## 1. Import Postman Collection

1. Mở Postman
2. Click **Import** ở góc trên bên trái
3. Chọn file `Todo_API_Postman_Collection.json`
4. Collection sẽ được import với tất cả các endpoints

## 2. Test Các Use Cases

### ✅ UC-01: Đăng ký tài khoản

**Request:** `POST /api/auth/register`

```json
{
  "email": "test@example.com",
  "name": "Test User",
  "password": "password123"
}
```

**Expected Response:** 201 Created
- Trả về thông tin user (không có password)
- User được lưu vào database

**Test Cases:**
- ✅ Đăng ký thành công
- ✅ Email đã tồn tại → 409 Conflict
- ✅ Email không hợp lệ → 422 Validation Error
- ✅ Password quá ngắn → 422 Validation Error

---

### ✅ UC-02: Đăng nhập hệ thống

**Request:** `POST /api/auth/login`

```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

**Expected Response:** 200 OK
- Trả về JWT access token
- Token có thời hạn 30 phút

**Test Cases:**
- ✅ Đăng nhập thành công
- ✅ Email/password sai → 401 Unauthorized
- ✅ Tài khoản bị khóa → 403 Forbidden

---

### ✅ UC-03: Tạo To-Do mới

**Request:** `POST /api/todos` (với Authorization header)

```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending",
  "priority": "high",
  "due_date": "2025-10-15T10:00:00"
}
```

**Expected Response:** 201 Created
- Trả về todo đã tạo với ID
- Todo gắn với user_id của người tạo

**Test Cases:**
- ✅ Tạo todo thành công
- ✅ Không có token → 403 Forbidden
- ✅ Token không hợp lệ → 401 Unauthorized
- ✅ Title rỗng → 422 Validation Error

---

### ✅ UC-04: Xem danh sách To-Do

**Request:** `GET /api/todos` (với Authorization header)

**Expected Response:** 200 OK
- Trả về danh sách todos của user hiện tại
- Không thấy todos của user khác

**Test Cases:**
- ✅ Lấy danh sách thành công
- ✅ Không có token → 403 Forbidden
- ✅ Chỉ thấy todos của mình

---

### ✅ UC-05: Cập nhật To-Do

**Request:** `PUT /api/todos/{id}` (với Authorization header)

```json
{
  "title": "Buy groceries - Updated",
  "status": "completed",
  "priority": "medium"
}
```

**Expected Response:** 200 OK
- Trả về todo đã cập nhật

**Test Cases:**
- ✅ Cập nhật thành công
- ✅ Todo không tồn tại → 404 Not Found
- ✅ Không có quyền (todo của user khác) → 403 Forbidden
- ✅ Token không hợp lệ → 401 Unauthorized

---

### ✅ UC-06: Xóa To-Do

**Request:** `DELETE /api/todos/{id}` (với Authorization header)

**Expected Response:** 200 OK
- Trả về message xác nhận
- Todo bị xóa khỏi database

**Test Cases:**
- ✅ Xóa thành công
- ✅ Todo không tồn tại → 404 Not Found
- ✅ Không có quyền (todo của user khác) → 403 Forbidden
- ✅ Token không hợp lệ → 401 Unauthorized

---

### ✅ UC-07: Tìm kiếm và lọc To-Do

**Filter by Status:**
```
GET /api/todos?status=pending
```

**Filter by Priority:**
```
GET /api/todos?priority=high
```

**Search:**
```
GET /api/todos?search=groceries
```

**Sort:**
```
GET /api/todos?sort_by=created_at&sort_order=asc
```

**Combined:**
```
GET /api/todos?status=pending&priority=high&search=buy&sort_by=due_date&sort_order=desc
```

**Test Cases:**
- ✅ Filter theo status
- ✅ Filter theo priority
- ✅ Search trong title và description
- ✅ Sort theo các trường khác nhau
- ✅ Kết hợp nhiều filters

---

### ✅ UC-08: Đăng xuất

**Request:** `POST /api/auth/logout` (với Authorization header)

**Expected Response:** 200 OK
- Token được thêm vào blacklist
- Không thể dùng token này nữa

**Test Cases:**
- ✅ Đăng xuất thành công
- ✅ Token đã blacklist không thể dùng → 401 Unauthorized

---

### ✅ UC-09: Quản lý người dùng (Admin)

**Admin Login:**
```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

**Get All Users:** `GET /api/admin/users`

**Block User:** `PUT /api/admin/users/{id}/block`

**Unblock User:** `PUT /api/admin/users/{id}/unblock`

**Delete User:** `DELETE /api/admin/users/{id}`

**Test Cases:**
- ✅ Admin xem được tất cả users
- ✅ Admin khóa/mở khóa user
- ✅ Admin xóa user (không phải admin)
- ✅ Không thể xóa admin
- ✅ User thường không truy cập được → 403 Forbidden

---

### ✅ UC-10: Xem thống kê hệ thống

**Request:** `GET /api/admin/stats` (với admin token)

**Expected Response:** 200 OK
```json
{
  "total_users": 5,
  "active_users": 4,
  "total_todos": 20,
  "completed_todos": 8,
  "pending_todos": 10
}
```

**Test Cases:**
- ✅ Admin xem thống kê thành công
- ✅ User thường không truy cập được → 403 Forbidden

---

## 3. Quy trình Test đầy đủ

### Bước 1: Authentication Flow
1. ✅ Register new user
2. ✅ Login → lưu token
3. ✅ Get current user info
4. ✅ Create admin (chạy script)
5. ✅ Admin login → lưu admin token

### Bước 2: Todo CRUD Flow
1. ✅ Create multiple todos
2. ✅ Get all todos
3. ✅ Get single todo
4. ✅ Update todo
5. ✅ Filter todos (status, priority)
6. ✅ Search todos
7. ✅ Delete todo

### Bước 3: Authorization Tests
1. ✅ Tạo user thứ 2
2. ✅ User 1 không thể sửa/xóa todo của User 2
3. ✅ Kiểm tra ownership validation

### Bước 4: Admin Flow
1. ✅ Admin login
2. ✅ View all users
3. ✅ Block/unblock user
4. ✅ View system stats
5. ✅ Try admin endpoints with regular user token

### Bước 5: Logout Flow
1. ✅ Logout user
2. ✅ Try to use blacklisted token → should fail

---

## 4. Automated Tests với pytest

Chạy tất cả tests:
```bash
pytest
```

Chạy test cụ thể:
```bash
pytest tests/test_auth.py -v
pytest tests/test_todos.py -v
pytest tests/test_admin.py -v
```

Chạy với coverage:
```bash
pytest --cov=app tests/
```

---

## 5. Performance Testing

### Test hiệu năng với 100 requests/phút:

```python
import time
import requests

base_url = "http://localhost:8000"

# Login
login = requests.post(f"{base_url}/api/auth/login", json={
    "email": "test@example.com",
    "password": "password123"
})
token = login.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Test 100 requests
start_time = time.time()
for i in range(100):
    response = requests.get(f"{base_url}/api/todos", headers=headers)
    print(f"Request {i+1}: {response.status_code} - {response.elapsed.total_seconds():.3f}s")

total_time = time.time() - start_time
print(f"\nTotal time: {total_time:.2f}s")
print(f"Average: {total_time/100:.3f}s per request")
```

**Expected:** P95 < 300ms

---

## 6. Kiểm tra Logs

Server logs mỗi request với format:
```
2025-10-14 19:09:58,649 - main - INFO - Request: GET /api/todos
2025-10-14 19:09:58,651 - main - INFO - Response: GET /api/todos - Status: 200 - Time: 0.002s
```

Kiểm tra:
- ✅ Mỗi request có 1 dòng log
- ✅ Log có timestamp
- ✅ Log có method, path, status, response time

---

## 7. Security Checklist

✅ **Password Security:**
- Password được hash với bcrypt
- Không trả về password trong response

✅ **JWT Security:**
- Token có expiration time
- Token được validate ở mọi protected endpoint

✅ **Authorization:**
- Chỉ owner mới sửa/xóa todo của mình
- Admin có quyền cao hơn

✅ **Token Blacklist:**
- Token bị vô hiệu hóa sau logout

✅ **SQL Injection:**
- Dùng ORM (SQLAlchemy) → safe

✅ **CORS:**
- Configured (production cần restrict origins)

---

## 8. Test Coverage

Kiểm tra coverage với pytest:
```bash
pytest --cov=app --cov-report=html tests/
```

Mở `htmlcov/index.html` để xem chi tiết coverage.

**Target:** > 80% coverage

---

## 9. API Documentation

Truy cập:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Ở đây bạn có thể:
- Xem tất cả endpoints
- Test trực tiếp trên browser
- Xem schemas và models

---

## 10. Troubleshooting

### Lỗi 401 Unauthorized
- Kiểm tra token có đúng không
- Token có hết hạn không (30 phút)
- Token có bị blacklist không

### Lỗi 403 Forbidden
- User có quyền không
- Có phải owner của resource không
- Có phải admin không (nếu cần)

### Lỗi 404 Not Found
- Resource có tồn tại không
- ID có đúng không

### Lỗi 422 Validation Error
- Kiểm tra format dữ liệu
- Kiểm tra required fields
- Kiểm tra data types

---

## 11. Kết quả mong đợi

✅ Tất cả 10 Use Cases hoạt động đúng  
✅ Authorization và Authentication hoạt động tốt  
✅ Performance đạt yêu cầu (< 300ms)  
✅ Logs đầy đủ cho mọi request  
✅ Tests pass 100%  
✅ Security đảm bảo (password hash, JWT, authorization)  
✅ API documentation đầy đủ  

---

## Credentials để test:

**Regular User:**
- Email: test@example.com
- Password: password123

**Admin User:**
- Email: admin@example.com
- Password: admin123

**Database:**
- Host: localhost:5432
- Database: todo_db
- Username: postgres
- Password: 123456
