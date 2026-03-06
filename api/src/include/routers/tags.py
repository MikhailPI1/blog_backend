from fastapi import APIRouter, HTTPException, status

from ..db.db_func import create_tag_query, get_tag_query, get_tag_by_slug_query,update_tag_query, delete_tag_query
from ..schemas.models import Tag, TagCreate, TagUpdate

router = APIRouter()


@router.post("/", response_model=Tag, status_code=status.HTTP_201_CREATED)
async def create_tag(tag_data: TagCreate):
    """Создает новый тег"""
    existing = await get_tag_by_slug_query(tag_data.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag with this slug already exists"
        )
    
    result = await create_tag_query(
        name=tag_data.name,
        slug=tag_data.slug
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create tag"
        )
    
    return Tag(**result)


@router.get("/{tag_id}", response_model=Tag)
async def get_tag(tag_id: int):
    """Получает тег по ID"""
    result = await get_tag_query(tag_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    
    return Tag(**result)


@router.get("/slug/{slug}", response_model=Tag)
async def get_tag_by_slug(slug: str):
    """Получает тег по slug"""
    result = await get_tag_by_slug_query(slug)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    
    return Tag(**result)


@router.patch("/{tag_id}", response_model=Tag)
async def update_tag(tag_id: int, tag_data: TagUpdate):
    """Обновляет тег"""
    existing = await get_tag_query(tag_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    
    result = await update_tag_query(
        tag_id=tag_id,
        name=tag_data.name,
        slug=tag_data.slug
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update tag"
        )
    
    return Tag(**result)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: int):
    """Удаляет тег"""
    existing = await get_tag_query(tag_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    
    result = await delete_tag_query(tag_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete tag"
        )
    
    return None