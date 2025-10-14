# To-Do API - Quản lý To-Do đa người dùng

REST API quản lý To-Do với xác thực JWT, được xây dựng với FastAPI và PostgreSQL.

## Tính năng

### Chức năng chính
- ✅ Đăng ký/Đăng nhập với JWT authentication
- ✅ CRUD To-Do (title, description, due_date, status, priority)
- ✅ Phân quyền: Mỗi user chỉ quản lý To-Do của mình
- ✅ Tìm kiếm và lọc To-Do (status, priority, search)
- ✅ Đăng xuất với token blacklist
- ✅ Admin: Quản lý người dùng và xem thống kê

### Yêu cầu phi chức năng
- ✅ Mã hóa password với bcrypt
- ✅ JWT token cho authentication
- ✅ Logging mỗi request
- ✅ CORS middleware
- ✅ Response time tracking

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Testing**: pytest

## Cài đặt

### 1. Yêu cầu hệ thống
- Python 3.8+
- PostgreSQL 12+

### 2. Clone repository
```bash
cd d:\KiemThuPhanMem
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình Database

Tạo database PostgreSQL:
```sql
CREATE DATABASE todo_db;
```

Cập nhật file `.env` (đã có sẵn):
```env
DATABASE_URL=postgresql://postgres:123456@localhost:5432/todo_db
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Chạy ứng dụng
```bash
python main.py
```

Hoặc với uvicorn:
```bash
uvicorn main:app --reload
```

API sẽ chạy tại: `http://localhost:8000`

## API Documentation

Sau khi chạy server, truy cập:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/register` - Đăng ký tài khoản mới
- `POST /api/auth/login` - Đăng nhập
- `POST /api/auth/logout` - Đăng xuất
- `GET /api/auth/me` - Lấy thông tin user hiện tại

### Todos
- `POST /api/todos` - Tạo To-Do mới
- `GET /api/todos` - Lấy danh sách To-Do (với filter & search)
- `GET /api/todos/{id}` - Lấy chi tiết To-Do
- `PUT /api/todos/{id}` - Cập nhật To-Do
- `DELETE /api/todos/{id}` - Xóa To-Do

### Admin
- `GET /api/admin/users` - Xem danh sách người dùng
- `PUT /api/admin/users/{id}/block` - Khóa người dùng
- `PUT /api/admin/users/{id}/unblock` - Mở khóa người dùng
- `DELETE /api/admin/users/{id}` - Xóa người dùng
- `GET /api/admin/stats` - Xem thống kê hệ thống

## Ví dụ sử dụng

### 1. Đăng ký
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "password123"
  }'
```

### 2. Đăng nhập
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Tạo To-Do
```bash
curl -X POST "http://localhost:8000/api/todos" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "pending",
    "priority": "high",
    "due_date": "2025-10-15T10:00:00"
  }'
```

### 4. Lấy danh sách To-Do với filter
```bash
curl -X GET "http://localhost:8000/api/todos?status=pending&priority=high&search=buy" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Testing

Chạy tests:
```bash
pytest
```

Chạy với coverage:
```bash
pytest --cov=app tests/
```

Chạy test cụ thể:
```bash
pytest tests/test_auth.py
pytest tests/test_todos.py
pytest tests/test_admin.py
```

## Cấu trúc Project

```
KiemThuPhanMem/
├── app/
│   ├── __init__.py
│   ├── auth.py           # Authentication & Authorization
│   ├── config.py         # Configuration settings
│   ├── database.py       # Database connection
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   └── routers/
│       ├── __init__.py
│       ├── auth.py       # Auth endpoints
│       ├── todos.py      # Todo endpoints
│       └── admin.py      # Admin endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # Test fixtures
│   ├── test_auth.py      # Auth tests
│   ├── test_todos.py     # Todo tests
│   └── test_admin.py     # Admin tests
├── .env                  # Environment variables
├── main.py               # Application entry point
├── requirements.txt      # Dependencies
└── README.md
```

## Database Schema

### Users Table
- `id`: Integer (PK)
- `email`: String (Unique)
- `name`: String
- `hashed_password`: String
- `role`: Enum (user, admin)
- `is_active`: Boolean
- `created_at`: DateTime
- `updated_at`: DateTime

### Todos Table
- `id`: Integer (PK)
- `title`: String
- `description`: Text
- `due_date`: DateTime
- `status`: Enum (pending, in_progress, completed)
- `priority`: Enum (low, medium, high)
- `user_id`: Integer (FK)
- `created_at`: DateTime
- `updated_at`: DateTime

### Token Blacklist Table
- `id`: Integer (PK)
- `token`: String (Unique)
- `user_id`: Integer (FK)
- `blacklisted_at`: DateTime

## Use Cases Implementation

✅ **UC-01**: Đăng ký tài khoản  
✅ **UC-02**: Đăng nhập hệ thống  
✅ **UC-03**: Tạo To-Do mới  
✅ **UC-04**: Xem danh sách To-Do  
✅ **UC-05**: Cập nhật To-Do  
✅ **UC-06**: Xóa To-Do  
✅ **UC-07**: Tìm kiếm và lọc To-Do  
✅ **UC-08**: Đăng xuất  
✅ **UC-09**: Quản lý người dùng (Admin)  
✅ **UC-10**: Xem thống kê hệ thống  

## Bảo mật

- ✅ Password được hash bằng bcrypt
- ✅ JWT token với expiration time
- ✅ Token blacklist khi logout
- ✅ Authorization kiểm tra ownership
- ✅ Role-based access control (Admin)
- ✅ SQL injection protection (ORM)
- ✅ CORS configuration

## Performance

- Request logging với timestamp
- Response time tracking
- Database connection pooling
- Efficient queries với SQLAlchemy

## Tạo Admin User

Để tạo admin user, bạn có thể:

1. Đăng ký user bình thường
2. Vào database và update role:

```sql
UPDATE users SET role = 'admin' WHERE email = 'admin@example.com';
```

Hoặc tạo script Python:

```python
from app.database import SessionLocal
from app.models import User, UserRole
from app.auth import get_password_hash

db = SessionLocal()
admin = User(
    email="admin@example.com",
    name="Admin",
    hashed_password=get_password_hash("admin123"),
    role=UserRole.ADMIN
)
db.add(admin)
db.commit()
```

## Troubleshooting

### Lỗi kết nối database
- Kiểm tra PostgreSQL đang chạy
- Kiểm tra credentials trong `.env`
- Đảm bảo database `todo_db` đã được tạo

### Import errors
- Chạy `pip install -r requirements.txt`
- Kiểm tra Python version (>= 3.8)

### Token expired
- Token có thời hạn 30 phút (cấu hình trong `.env`)
- Đăng nhập lại để lấy token mới

## License

MIT License
