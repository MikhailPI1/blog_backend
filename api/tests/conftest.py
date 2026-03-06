import pytest
import json
import time
from httpx import AsyncClient
from src.main import app
from src.db.db_func import get_post_query, delete_post_query
from src.cach.redis_connect import r


@pytest.fixture
async def client():
    """Фикстура для HTTP клиента"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_post_data():
    """Тестовые данные для поста"""
    return {
        "slug": "test-post",
        "title": "Test Post",
        "content": "This is test content",
        "user_id": 1,
        "excerpt": "Test excerpt",
        "status": "published",
        "is_featured": False
    }


@pytest.mark.asyncio
async def test_create_post(client, test_post_data):
    """Тест создания поста"""
    response = await client.post("/api/posts/", json=test_post_data)
    assert response.status_code == 201
    data = response.json()
    assert data["slug"] == test_post_data["slug"]
    assert data["title"] == test_post_data["title"]
    assert "id" in data
    return data["id"]


@pytest.mark.asyncio
async def test_get_post_cache(client, test_post_data):
    """Тест кеширования при GET запросе"""
    create_resp = await client.post("/api/posts/", json=test_post_data)
    post_id = create_resp.json()["id"]
    
    r.delete(f"post:{post_id}")

    response1 = await client.get(f"/api/posts/{post_id}")
    assert response1.status_code == 200
    
    cached = r.hget(f"post:{post_id}", "data")
    assert cached is not None
    cached_data = json.loads(cached)
    assert cached_data["id"] == post_id
    
    start = time.time()
    response2 = await client.get(f"/api/posts/{post_id}")
    end = time.time()
    
    assert response2.status_code == 200
    assert response2.json()["id"] == post_id

    await delete_post_query(post_id)


@pytest.mark.asyncio
async def test_update_post_invalidates_cache(client, test_post_data):
    """Тест что при обновлении поста кеш инвалидируется"""
    create_resp = await client.post("/api/posts/", json=test_post_data)
    post_id = create_resp.json()["id"]
    
    await client.get(f"/api/posts/{post_id}")
    
    cached_before = r.hget(f"post:{post_id}", "data")
    assert cached_before is not None
    
    update_data = {"title": "Updated Title"}
    response = await client.patch(f"/api/posts/{post_id}", json=update_data)
    assert response.status_code == 200
    
    cached_after = r.hget(f"post:{post_id}", "data")
    assert cached_after is None
    
    response = await client.get(f"/api/posts/{post_id}")
    assert response.status_code == 200
    
    cached_new = r.hget(f"post:{post_id}", "data")
    assert cached_new is not None
    cached_data = json.loads(cached_new)
    assert cached_data["title"] == "Updated Title"
    
    await delete_post_query(post_id)


@pytest.mark.asyncio
async def test_delete_post_invalidates_cache(client, test_post_data):
    """Тест что при удалении поста кеш инвалидируется"""
    create_resp = await client.post("/api/posts/", json=test_post_data)
    post_id = create_resp.json()["id"]
    
    await client.get(f"/api/posts/{post_id}")
    
    cached_before = r.hget(f"post:{post_id}", "data")
    assert cached_before is not None
    
    response = await client.delete(f"/api/posts/{post_id}")
    assert response.status_code == 204
    
    cached_after = r.hget(f"post:{post_id}", "data")
    assert cached_after is None
    
    response = await client.get(f"/api/posts/{post_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_post_by_slug_cache(client, test_post_data):
    """Тест кеширования при GET по slug"""
    create_resp = await client.post("/api/posts/", json=test_post_data)
    post_id = create_resp.json()["id"]
    slug = test_post_data["slug"]
    
    r.delete(f"post:slug:{slug}")
    
    response1 = await client.get(f"/api/posts/slug/{slug}")
    assert response1.status_code == 200
    
    cached_slug = r.hget(f"post:slug:{slug}", "data")
    assert cached_slug is not None
    
    await delete_post_query(post_id)


@pytest.mark.asyncio
async def test_cache_ttl(client, test_post_data):
    """Тест что TTL работает (кеш протухает)"""
    create_resp = await client.post("/api/posts/", json=test_post_data)
    post_id = create_resp.json()["id"]
    
    await client.get(f"/api/posts/{post_id}")
    
    ttl = r.ttl(f"post:{post_id}")
    assert ttl > 0
    assert ttl <= 86400
    
    await delete_post_query(post_id)
