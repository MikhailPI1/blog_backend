import json
from typing import Any, Awaitable, Callable, Dict, Optional, List

from .redis_connect import r

def cache_get_user(func: Callable[[int], Awaitable[Optional[Dict[str, Any]]]]):
    """Кеширует результат get_user_query"""
    async def cache_get_user_wrapper(user_id: int) -> Optional[Dict[str, Any]]:
        cache_key = f"user:{user_id}"
        print("cache_key:" + cache_key)
        cached = r.hget(cache_key, "data")
        if cached:
            r.expire(cache_key, 86400)
            return json.loads(cached) if cached else None
        
        result = await func(user_id)
        
        if result and result.get('id'):
            r.hset(cache_key, "data", json.dumps(result, default=str))
            r.expire(cache_key, 86400)
        
        return result
    return cache_get_user_wrapper

def cache_get_user_by_email(func: Callable[[str], Awaitable[Optional[Dict[str, Any]]]]):
    """Кеширует результат get_user_by_email_query"""
    async def cache_get_user_by_email_wrapper(email: str) -> Optional[Dict[str, Any]]:
        cache_key = f"user:email:{email}"
        cached = r.hget(cache_key, "data")
        print("cache_key:" + cached)
        if cached:
            r.expire(cache_key, 86400)
            return json.loads(cached) if cached else None
        
        result = await func(email)
        
        if result and result.get('id'):
            r.hset(cache_key, "data", json.dumps(result, default=str))
            r.expire(cache_key, 86400)
        
        return result
    return cache_get_user_by_email_wrapper

def cache_get_post(func: Callable[[int], Awaitable[Optional[Dict[str, Any]]]]):
    """Кеширует результат get_post_query"""
    async def cache_get_post_wrapper(post_id: int) -> Optional[Dict[str, Any]]:
        cache_key = f"post:{post_id}"
        cached = r.hget(cache_key, "data")
        if cached:
            r.expire(cache_key, 86400)
            return json.loads(cached) if cached else None
        
        result = await func(post_id)
        
        if result:
            r.hset(cache_key, "data", json.dumps(result, default=str))
            r.expire(cache_key, 86400)
        
        return result
    return cache_get_post_wrapper

def cache_get_post_by_slug(func: Callable[[str], Awaitable[Optional[Dict[str, Any]]]]):
    """Кеширует результат get_post_by_slug_query"""
    async def cache_get_post_by_slug_wrapper(slug: str) -> Optional[Dict[str, Any]]:
        cache_key = f"post:slug:{slug}"
        cached = r.hget(cache_key, "data")
        if cached:
            r.expire(cache_key, 86400)
            return json.loads(cached) if cached else None
        
        result = await func(slug)
        
        if result:
            r.hset(cache_key, "data", json.dumps(result, default=str))
            r.expire(cache_key, 86400)
        
        return result
    return cache_get_post_by_slug_wrapper

def cache_get_category(func: Callable[[int], Awaitable[Optional[Dict[str, Any]]]]):
    """Кеширует результат get_category_query"""
    async def cache_get_category_wrapper(category_id: int) -> Optional[Dict[str, Any]]:
        cache_key = f"category:{category_id}"
        cached = r.hget(cache_key, "data")
        if cached:
            r.expire(cache_key, 86400)
            return json.loads(cached) if cached else None
        
        result = await func(category_id)
        
        if result:
            r.hset(cache_key, "data", json.dumps(result, default=str))
            r.expire(cache_key, 86400)
        
        return result
    return cache_get_category_wrapper

def cache_get_category_with_children(func: Callable[[int], Awaitable[Optional[Dict[str, Any]]]]):
    """Кеширует результат get_category_with_children_query"""
    async def cache_get_category_with_children_wrapper(category_id: int) -> Optional[Dict[str, Any]]:
        cache_key = f"category:tree:{category_id}"
        cached = r.hget(cache_key, "data")
        if cached:
            r.expire(cache_key, 86400)
            return json.loads(cached) if cached else None
        
        result = await func(category_id)
        
        if result:
            r.hset(cache_key, "data", json.dumps(result, default=str))
            r.expire(cache_key, 86400)
        
        return result
    return cache_get_category_with_children_wrapper

def cache_get_tag(func: Callable[[int], Awaitable[Optional[Dict[str, Any]]]]):
    """Кеширует результат get_tag_query"""
    async def cache_get_tag_wrapper(tag_id: int) -> Optional[Dict[str, Any]]:
        cache_key = f"tag:{tag_id}"
        cached = r.hget(cache_key, "data")
        if cached:
            r.expire(cache_key, 86400)
            return json.loads(cached) if cached else None
        
        result = await func(tag_id)
        
        if result:
            r.hset(cache_key, "data", json.dumps(result, default=str))
            r.expire(cache_key, 86400)
        
        return result
    return cache_get_tag_wrapper

def cache_get_tag_by_slug(func: Callable[[str], Awaitable[Optional[Dict[str, Any]]]]):
    """Кеширует результат get_tag_by_slug_query"""
    async def cache_get_tag_by_slug_wrapper(slug: str) -> Optional[Dict[str, Any]]:
        cache_key = f"tag:slug:{slug}"
        cached = r.hget(cache_key, "data")
        if cached:
            r.expire(cache_key, 86400)
            return json.loads(cached) if cached else None
        
        result = await func(slug)
        
        if result:
            r.hset(cache_key, "data", json.dumps(result, default=str))
            r.expire(cache_key, 86400)
        
        return result
    return cache_get_tag_by_slug_wrapper

def cache_get_post_tags(func: Callable[[int], Awaitable[List[Dict[str, Any]]]]):
    """Кеширует результат get_post_tags_query"""
    async def cache_get_post_tags_wrapper(post_id: int) -> List[Dict[str, Any]]:
        cache_key = f"post:tags:{post_id}"
        cached = r.hget(cache_key, "data")
        if cached:
            r.expire(cache_key, 86400)
            return json.loads(cached) if cached else []
        
        result = await func(post_id)
        
        if result:
            r.hset(cache_key, "data", json.dumps(result, default=str))
            r.expire(cache_key, 86400)
        
        return result
    return cache_get_post_tags_wrapper

def cache_get_tag_posts(func: Callable[[int], Awaitable[List[Dict[str, Any]]]]):
    """Кеширует результат get_tag_posts_query"""
    async def cache_get_tag_posts_wrapper(tag_id: int) -> List[Dict[str, Any]]:
        cache_key = f"tag:posts:{tag_id}"
        cached = r.hget(cache_key, "data")
        if cached:
            r.expire(cache_key, 86400)
            return json.loads(cached) if cached else []
        
        result = await func(tag_id)
        
        if result:
            r.hset(cache_key, "data", json.dumps(result, default=str))
            r.expire(cache_key, 86400)
        
        return result
    return cache_get_tag_posts_wrapper

def cache_get_post_categories(func: Callable[[int], Awaitable[List[Dict[str, Any]]]]):
    """Кеширует результат get_post_categories_query"""
    async def cache_get_post_categories_wrapper(post_id: int) -> List[Dict[str, Any]]:
        cache_key = f"post:categories:{post_id}"
        cached = r.hget(cache_key, "data")
        if cached:
            r.expire(cache_key, 86400)
            return json.loads(cached) if cached else []
        
        result = await func(post_id)
        
        if result:
            r.hset(cache_key, "data", json.dumps(result, default=str))
            r.expire(cache_key, 86400)
        
        return result
    return cache_get_post_categories_wrapper

def invalidate_user_cache(func: Callable):
    """Инвалидирует кэш пользователя при удалении/обновлении"""
    async def invalidate_user_cache_wrapper(user_id: int, *args, **kwargs):
        result = await func(user_id, *args, **kwargs)
        
        if result:
            r.delete(f"user:{user_id}")

        return result
    return invalidate_user_cache_wrapper


def invalidate_post_cache(func: Callable):
    """Инвалидирует кэш поста при удалении/обновлении"""
    async def invalidate_post_cache_wrapper(post_id: int, *args, **kwargs):
        result = await func(post_id, *args, **kwargs)
        
        if result:
            r.delete(f"post:{post_id}")
            r.delete(f"post:tags:{post_id}")
            r.delete(f"post:categories:{post_id}")
        
        return result
    return invalidate_post_cache_wrapper


def invalidate_category_cache(func: Callable):
    """Инвалидирует кэш категории при удалении/обновлении"""
    async def invalidate_category_cache_wrapper(category_id: int, *args, **kwargs):

        result = await func(category_id, *args, **kwargs)
        
        if result:
            r.delete(f"category:{category_id}")
            r.delete(f"category:tree:{category_id}")
        
        return result
    return invalidate_category_cache_wrapper


def invalidate_tag_cache(func: Callable):
    """Инвалидирует кэш тега при удалении/обновлении"""
    async def invalidate_tag_cache_wrapper(tag_id: int, *args, **kwargs):

        result = await func(tag_id, *args, **kwargs)
        
        if result:
            r.delete(f"tag:{tag_id}")
            r.delete(f"tag:posts:{tag_id}")
        
        return result
    return invalidate_tag_cache_wrapper
