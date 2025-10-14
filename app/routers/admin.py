from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models import User, Todo, TodoStatus, UserRole
from app.schemas import UserAdminResponse, SystemStats
from app.auth import get_current_admin_user
import logging

router = APIRouter(prefix="/api/admin", tags=["Admin"])
logger = logging.getLogger(__name__)

@router.get("/users", response_model=List[UserAdminResponse])
def get_all_users(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """UC-09: Quản lý người dùng (Admin) - View all users"""
    logger.info(f"Admin {current_admin.email} fetching all users")
    
    users = db.query(User).all()
    logger.info(f"Retrieved {len(users)} users")
    return users

@router.put("/users/{user_id}/block")
def block_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """UC-09: Quản lý người dùng (Admin) - Block user"""
    logger.info(f"Admin {current_admin.email} blocking user {user_id}")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot block admin users"
        )
    
    user.is_active = False
    db.commit()
    
    logger.info(f"User {user_id} blocked successfully")
    return {"message": f"User {user.email} has been blocked"}

@router.put("/users/{user_id}/unblock")
def unblock_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """UC-09: Quản lý người dùng (Admin) - Unblock user"""
    logger.info(f"Admin {current_admin.email} unblocking user {user_id}")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = True
    db.commit()
    
    logger.info(f"User {user_id} unblocked successfully")
    return {"message": f"User {user.email} has been unblocked"}

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """UC-09: Quản lý người dùng (Admin) - Delete user"""
    logger.info(f"Admin {current_admin.email} deleting user {user_id}")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete admin users"
        )
    
    db.delete(user)
    db.commit()
    
    logger.info(f"User {user_id} deleted successfully")
    return {"message": f"User {user.email} has been deleted"}

@router.get("/stats", response_model=SystemStats)
def get_system_stats(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """UC-10: Xem thống kê hệ thống"""
    logger.info(f"Admin {current_admin.email} fetching system stats")
    
    total_users = db.query(func.count(User.id)).scalar()
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
    total_todos = db.query(func.count(Todo.id)).scalar()
    completed_todos = db.query(func.count(Todo.id)).filter(Todo.status == TodoStatus.COMPLETED).scalar()
    pending_todos = db.query(func.count(Todo.id)).filter(Todo.status == TodoStatus.PENDING).scalar()
    
    stats = {
        "total_users": total_users,
        "active_users": active_users,
        "total_todos": total_todos,
        "completed_todos": completed_todos,
        "pending_todos": pending_todos
    }
    
    logger.info("System stats retrieved successfully")
    return stats
