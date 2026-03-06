from fastapi import APIRouter, HTTPException, status

from ..db.db_func import get_post_by_slug_query, create_post_query, get_post_query, update_post_query,delete_post_query
from ..schemas.models import Post, PostCreate, PostUpdate

router = APIRouter()


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate):
    """Создает новый пост"""
    existing = await get_post_by_slug_query(post_data.slug)
    if existing and existing.get('id') is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post with this slug already exists"
        )
    
    result = await create_post_query(
        slug=post_data.slug,
        title=post_data.title,
        content=post_data.content,
        user_id=post_data.user_id,
        excerpt=post_data.excerpt,
        status=post_data.status,
        is_featured=post_data.is_featured,
        published_at=post_data.published_at
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create post"
        )
    
    return Post(**result)


@router.get("/{post_id}", response_model=Post)
async def get_post(post_id: int):
    """Получает пост по ID"""
    result = await get_post_query(post_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    return Post(**result)


@router.get("/slug/{slug}", response_model=Post)
async def get_post_by_slug(slug: str):
    """Получает пост по slug"""
    result = await get_post_by_slug_query(slug)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    return Post(**result)


@router.patch("/{post_id}", response_model=Post)
async def update_post(post_id: int, post_data: PostUpdate):
    """Обновляет пост"""
    # Проверяем существование
    existing = await get_post_query(post_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    result = await update_post_query(
        post_id=post_id,
        title=post_data.title,
        content=post_data.content,
        excerpt=post_data.excerpt,
        status=post_data.status,
        is_featured=post_data.is_featured
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update post"
        )
    
    return Post(**result)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    """Удаляет пост"""
    existing = await get_post_query(post_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    result = await delete_post_query(post_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete post"
        )
    
    return None