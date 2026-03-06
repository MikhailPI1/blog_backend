from . import db_connect as db
from ..cach import cach_func as cach
from ..log import log

from typing import Optional, Any, Dict, List, Tuple
from datetime import datetime

@log.async_logger
async def create_user_query(
    username: str,
    email: str,
    password_hash: str,
    bio: Optional[str] = None,
    avatar_url: Optional[str] = None,
    role: str = 'user'
) -> Optional[Dict[str, Any]]:
    """Создает нового пользователя."""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM create_user($1, $2, $3, $4, $5, $6)",
            username, email, password_hash, bio, avatar_url, role
        )
    return dict(row) if row else None

@log.async_logger
@cach.cache_get_user
async def get_user_query(user_id: int) -> Optional[Dict[str, Any]]:
    """Получает пользователя по ID."""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM get_user($1)",
            user_id
        )
    return dict(row) if row else None

@log.async_logger
async def get_user_by_email_query(email: str) -> Optional[Dict[str, Any]]:
    """Получает пользователя по email."""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM get_user_by_email($1)",
            email
        )
    return dict(row) if row else None

@log.async_logger
async def update_user_query(
    user_id: int,
    username: Optional[str] = None,
    bio: Optional[str] = None,
    avatar_url: Optional[str] = None,
    role: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Обновляет данные пользователя."""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM update_user($1, $2, $3, $4, $5)",
            user_id, username, bio, avatar_url, role
        )
    return dict(row) if row else None

@log.async_logger
@cach.invalidate_user_cache
async def delete_user_query(user_id: int) -> bool:
    """Удаляет пользователя."""
    async with db.pool.acquire() as conn:
        result = await conn.fetchval(
            "SELECT delete_user($1)",
            user_id
        )
    return result

@log.async_logger
async def create_post_query(
    slug: str,
    title: str,
    content: str,
    user_id: int,
    excerpt: Optional[str] = None,
    status: str = 'draft',
    is_featured: bool = False,
    published_at: Optional[datetime] = None
) -> Optional[Dict[str, Any]]:
    """Создает новый пост."""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM create_post($1, $2, $3, $4, $5, $6, $7, $8)",
            slug, title, content, user_id, excerpt, status, is_featured, published_at
        )
    return dict(row) if row else None

@log.async_logger
@cach.cache_get_post
async def get_post_query(post_id: int) -> Optional[Dict[str, Any]]:
    """Получает пост по ID."""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM get_post($1)",
            post_id
        )
    return dict(row) if row else None

@log.async_logger
@cach.cache_get_post_by_slug
async def get_post_by_slug_query(slug: str) -> Optional[Dict[str, Any]]:
    """Получает пост по slug."""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM get_post_by_slug($1)",
            slug
        )
    return dict(row) if row else None

@log.async_logger
async def update_post_query(
    post_id: int,
    title: Optional[str] = None,
    content: Optional[str] = None,
    excerpt: Optional[str] = None,
    status: Optional[str] = None,
    is_featured: Optional[bool] = None
) -> Optional[Dict[str, Any]]:
    """Обновляет пост."""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM update_post($1, $2, $3, $4, $5, $6)",
            post_id, title, content, excerpt, status, is_featured
        )
    return dict(row) if row else None

@log.async_logger
@cach.invalidate_post_cache
async def delete_post_query(post_id: int) -> bool:
    """Удаляет пост."""
    async with db.pool.acquire() as conn:
        result = await conn.fetchval(
            "SELECT delete_post($1)",
            post_id
        )
    return result

@log.async_logger
async def create_category_query(
    name: str,
    slug: str,
    description: Optional[str] = None,
    parent_id: Optional[int] = None,
    sort_order: int = 0
) -> Optional[Dict[str, Any]]:
    """Создает новую категорию."""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM create_category($1, $2, $3, $4, $5)",
            name, slug, description, parent_id, sort_order
        )
    return dict(row) if row else None

@log.async_logger
@cach.cache_get_category
async def get_category_query(category_id: int) -> Optional[Dict[str, Any]]:
    """Получает категорию по ID."""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM get_category($1)",
            category_id
        )
    return dict(row) if row else None

@log.async_logger
@cach.cache_get_category_with_children
async def get_category_with_children_query(category_id: int) -> Optional[Dict[str, Any]]:
    """Получает категорию с дочерними категориями."""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM get_category_with_children($1)",
            category_id
        )
    return dict(row) if row else None

@log.async_logger
async def update_category_query(
    category_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    parent_id: Optional[int] = None,
    sort_order: Optional[int] = None
) -> Optional[Dict[str, Any]]:
    """Обновляет категорию."""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM update_category($1, $2, $3, $4, $5)",
            category_id, name, description, parent_id, sort_order
        )
    return dict(row) if row else None

@log.async_logger
@cach.invalidate_category_cache
async def delete_category_query(category_id: int) -> bool:
    """Удаляет категорию."""
    async with db.pool.acquire() as conn:
        result = await conn.fetchval(
            "SELECT delete_category($1)",
            category_id
        )
    return result

@log.async_logger
async def create_tag_query(name: str, slug: str) -> Optional[Dict[str, Any]]:
    """Создает новый тег."""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM create_tag($1, $2)",
            name, slug
        )
    return dict(row) if row else None

@log.async_logger
@cach.cache_get_tag
async def get_tag_query(tag_id: int) -> Optional[Dict[str, Any]]:
    """Получает тег по ID."""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM get_tag($1)",
            tag_id
        )
    return dict(row) if row else None

@log.async_logger
@cach.cache_get_tag_by_slug
async def get_tag_by_slug_query(slug: str) -> Optional[Dict[str, Any]]:
    """Получает тег по slug."""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM get_tag_by_slug($1)",
            slug
        )
    return dict(row) if row else None

@log.async_logger
async def update_tag_query(
    tag_id: int,
    name: Optional[str] = None,
    slug: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Обновляет тег."""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM update_tag($1, $2, $3)",
            tag_id, name, slug
        )
    return dict(row) if row else None

@log.async_logger
@cach.invalidate_tag_cache
async def delete_tag_query(tag_id: int) -> bool:
    """Удаляет тег."""
    async with db.pool.acquire() as conn:
        result = await conn.fetchval(
            "SELECT delete_tag($1)",
            tag_id
        )
    return result

@log.async_logger
@cach.cache_get_post_tags
async def get_post_tags_query(post_id: int) -> List[Dict[str, Any]]:
    """Получает теги поста."""
    async with db.pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT * FROM get_post_tags($1)",
            post_id
        )
    return [dict(row) for row in rows]

@log.async_logger
@cach.cache_get_tag_posts
async def get_tag_posts_query(tag_id: int) -> List[Dict[str, Any]]:
    """Получает посты по тегу."""
    async with db.pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT * FROM get_tag_posts($1)",
            tag_id
        )
    return [dict(row) for row in rows]

@log.async_logger
async def create_post_view_query(
    post_id: int,
    user_id: Optional[int] = None,
    viewer_ip: Optional[str] = None,
    user_agent: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Создает просмотр поста"""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """INSERT INTO post_views (post_id, user_id, viewer_ip, user_agent) 
               VALUES ($1, $2, $3, $4) RETURNING *""",
            post_id, user_id, viewer_ip, user_agent
        )
    return dict(row) if row else None

@log.async_logger
async def get_post_views_query(post_id: int) -> List[Dict[str, Any]]:
    """Получает просмотры поста"""
    async with db.pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT * FROM post_views WHERE post_id = $1 ORDER BY viewed_at DESC",
            post_id
        )
    return [dict(row) for row in rows]

@log.async_logger
async def get_post_views_count_query(post_id: int) -> int:
    """Получает количество просмотров поста"""
    async with db.pool.acquire() as conn:
        result = await conn.fetchval(
            "SELECT COUNT(*) FROM post_views WHERE post_id = $1",
            post_id
        )
    return result or 0


@log.async_logger
async def assign_tag_to_post_query(post_id: int, tag_id: int) -> Optional[Dict[str, Any]]:
    """Присваивает тег посту - вызывает SQL функцию assign_tag_to_post"""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM assign_tag_to_post($1, $2)",
            post_id, tag_id
        )
    return dict(row) if row else None