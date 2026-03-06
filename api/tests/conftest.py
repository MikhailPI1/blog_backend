import pytest
from httpx import AsyncClient
from src.main import app


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
