from fastapi import APIRouter, HTTPException, status

from ..db.db_func import create_user_query, get_user_query, get_user_by_email_query,update_user_query, delete_user_query
from ..schemas.models import User, UserCreate, UserUpdate

router = APIRouter()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    """Создает нового пользователя"""
    existing = await get_user_by_email_query(user_data.email)
    if existing and existing.get('id') is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    result = await create_user_query(
        username=user_data.username,
        email=user_data.email,
        password_hash=user_data.password_hash,
        bio=user_data.bio,
        avatar_url=user_data.avatar_url,
        role=user_data.role
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )
    
    return User(**result)


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Получает пользователя по ID"""
    result = await get_user_query(user_id)
    
    if not result and result.get('id') is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return User(**result)


@router.get("/email/{email}", response_model=User)
async def get_user_by_email(email: str):
    """Получает пользователя по email"""
    result = await get_user_by_email_query(email)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return User(**result)


@router.patch("/{user_id}", response_model=User)
async def update_user(user_id: int, user_data: UserUpdate):
    """Обновляет данные пользователя"""
    existing = await get_user_query(user_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    result = await update_user_query(
        user_id=user_id,
        username=user_data.username,
        bio=user_data.bio,
        avatar_url=user_data.avatar_url,
        role=user_data.role
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )
    
    return User(**result)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """Удаляет пользователя"""
    existing = await get_user_query(user_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    result = await delete_user_query(user_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )
    
    return None