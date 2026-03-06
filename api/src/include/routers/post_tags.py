from fastapi import APIRouter, HTTPException, status
from typing import List

from ..db import db_connect as db
from ..db.db_func import assign_tag_to_post_query, get_post_tags_query, get_tag_posts_query
from ..schemas.models import PostTag, PostTagResult, TagPostResult

router = APIRouter()


@router.post("/posts/{post_id}/tags/{tag_id}", response_model=PostTag)
async def assign_tag_to_post(post_id: int, tag_id: int):
    """Присваивает тег посту"""
    existing_tags = await get_post_tags_query(post_id)
    if any(t['tag_id'] == tag_id for t in existing_tags):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag already assigned to this post"
        )
    
    result = await assign_tag_to_post_query(post_id, tag_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to assign tag to post"
        )
    
    return PostTag(**result)


@router.get("/posts/{post_id}/tags", response_model=List[PostTagResult])
async def get_post_tags(post_id: int):
    """Получает все теги поста"""
    result = await get_post_tags_query(post_id)
    return [PostTagResult(**item) for item in result]


@router.get("/tags/{tag_id}/posts", response_model=List[TagPostResult])
async def get_tag_posts(tag_id: int):
    """Получает все посты с тегом"""
    result = await get_tag_posts_query(tag_id)
    return [TagPostResult(**item) for item in result]


@router.delete("/posts/{post_id}/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_tag_from_post(post_id: int, tag_id: int):
    """Удаляет тег у поста"""
    async with db.pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM post_tags WHERE post_id = $1 AND tag_id = $2",
            post_id, tag_id
        )
    
    if result == "DELETE 0":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found on this post"
        )
    
    return None