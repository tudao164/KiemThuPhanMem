from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models import User, Todo, TodoStatus, TodoPriority
from app.schemas import TodoCreate, TodoUpdate, TodoResponse
from app.auth import get_current_user
import logging

router = APIRouter(prefix="/api/todos", tags=["Todos"])
logger = logging.getLogger(__name__)

@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """UC-03: Tạo To-Do mới"""
    logger.info(f"Creating todo for user: {current_user.email}")
    
    new_todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        due_date=todo_data.due_date,
        status=todo_data.status,
        priority=todo_data.priority,
        user_id=current_user.id
    )
    
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    logger.info(f"Todo created successfully: ID {new_todo.id} for user {current_user.email}")
    return new_todo

@router.get("", response_model=List[TodoResponse])
def get_todos(
    status: Optional[TodoStatus] = Query(None, description="Filter by status"),
    priority: Optional[TodoPriority] = Query(None, description="Filter by priority"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    sort_by: Optional[str] = Query("created_at", description="Sort by field"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """UC-04 & UC-07: Xem danh sách To-Do và Tìm kiếm/lọc"""
    logger.info(f"Fetching todos for user: {current_user.email}")
    
    query = db.query(Todo).filter(Todo.user_id == current_user.id)
    
    # Apply filters
    if status:
        query = query.filter(Todo.status == status)
    
    if priority:
        query = query.filter(Todo.priority == priority)
    
    if search:
        search_filter = or_(
            Todo.title.ilike(f"%{search}%"),
            Todo.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Apply sorting
    valid_sort_fields = ["created_at", "updated_at", "due_date", "priority", "status"]
    if sort_by not in valid_sort_fields:
        sort_by = "created_at"
    
    sort_column = getattr(Todo, sort_by)
    if sort_order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
    
    todos = query.all()
    logger.info(f"Retrieved {len(todos)} todos for user {current_user.email}")
    return todos

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get single todo by ID"""
    logger.info(f"Fetching todo {todo_id} for user: {current_user.email}")
    
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not todo:
        logger.warning(f"Todo {todo_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    if todo.user_id != current_user.id:
        logger.warning(f"User {current_user.email} unauthorized to access todo {todo_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this todo"
        )
    
    return todo

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """UC-05: Cập nhật To-Do"""
    logger.info(f"Updating todo {todo_id} for user: {current_user.email}")
    
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not todo:
        logger.warning(f"Todo {todo_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    if todo.user_id != current_user.id:
        logger.warning(f"User {current_user.email} unauthorized to update todo {todo_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this todo"
        )
    
    # Update fields
    update_data = todo_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)
    
    todo.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(todo)
    
    logger.info(f"Todo {todo_id} updated successfully")
    return todo

@router.delete("/{todo_id}", status_code=status.HTTP_200_OK)
def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """UC-06: Xóa To-Do"""
    logger.info(f"Deleting todo {todo_id} for user: {current_user.email}")
    
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not todo:
        logger.warning(f"Todo {todo_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    if todo.user_id != current_user.id:
        logger.warning(f"User {current_user.email} unauthorized to delete todo {todo_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this todo"
        )
    
    db.delete(todo)
    db.commit()
    
    logger.info(f"Todo {todo_id} deleted successfully")
    return {"message": "Todo deleted successfully"}
