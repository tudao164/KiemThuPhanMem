# Script để tạo admin user
from app.database import SessionLocal
from app.models import User, UserRole
from app.auth import get_password_hash

def create_admin():
    db = SessionLocal()
    
    # Check if admin exists
    existing_admin = db.query(User).filter(User.email == "admin@example.com").first()
    if existing_admin:
        print("Admin user already exists!")
        db.close()
        return
    
    # Create admin user
    admin = User(
        email="admin@example.com",
        name="Admin User",
        hashed_password=get_password_hash("admin123"),
        role=UserRole.ADMIN,
        is_active=True
    )
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    print(f"Admin user created successfully!")
    print(f"Email: {admin.email}")
    print(f"Password: admin123")
    print(f"Role: {admin.role}")
    
    db.close()

if __name__ == "__main__":
    create_admin()
