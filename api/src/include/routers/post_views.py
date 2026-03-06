from fastapi import APIRouter, HTTPException, status, Request
from typing import List, Optional

from ..db.db_func import create_post_view_query, get_post_views_query, get_post_views_count_query
from ..schemas.models import PostViewResult

router = APIRouter()


@router.post("/posts/{post_id}", response_model=PostViewResult)
async def create_post_view(
    post_id: int, 
    request: Request,
    user_id: Optional[int] = None
):
    """Создает просмотр поста"""
    viewer_ip = request.client.host
    user_agent = request.headers.get("user-agent")
    
    result = await create_post_view_query(
        post_id=post_id,
        user_id=user_id,
        viewer_ip=viewer_ip,
        user_agent=user_agent
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create post view"
        )
    
    return PostViewResult(**result)


@router.get("/posts/{post_id}", response_model=List[PostViewResult])
async def get_post_views(post_id: int):
    """Получает все просмотры поста"""
    result = await get_post_views_query(post_id)
    return [PostViewResult(**item) for item in result]


@router.get("/posts/{post_id}/count", response_model=int)
async def get_post_views_count(post_id: int):
    """Получает количество просмотров поста"""
    result = await get_post_views_count_query(post_id)
    return result