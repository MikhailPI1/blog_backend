from fastapi import APIRouter, HTTPException, status

from ..db.db_func import create_category_query, get_category_query, get_category_with_children_query,update_category_query, delete_category_query
from ..schemas.models import Category, CategoryCreate, CategoryUpdate, CategoryWithChildren

router = APIRouter()


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(category_data: CategoryCreate):
    """Создает новую категорию"""
    result = await create_category_query(
        name=category_data.name,
        slug=category_data.slug,
        description=category_data.description,
        parent_id=category_data.parent_id,
        sort_order=category_data.sort_order
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create category"
        )
    
    return Category(**result)


@router.get("/{category_id}", response_model=Category)
async def get_category(category_id: int):
    """Получает категорию по ID"""
    result = await get_category_query(category_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return Category(**result)


@router.get("/{category_id}/with-children", response_model=CategoryWithChildren)
async def get_category_with_children(category_id: int):
    """Получает категорию с дочерними категориями"""
    result = await get_category_with_children_query(category_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return CategoryWithChildren(**result)


@router.patch("/{category_id}", response_model=Category)
async def update_category(category_id: int, category_data: CategoryUpdate):
    """Обновляет категорию"""
    existing = await get_category_query(category_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    result = await update_category_query(
        category_id=category_id,
        name=category_data.name,
        description=category_data.description,
        parent_id=category_data.parent_id,
        sort_order=category_data.sort_order
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update category"
        )
    
    return Category(**result)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int):
    """Удаляет категорию"""
    existing = await get_category_query(category_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    result = await delete_category_query(category_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete category"
        )
    
    return None