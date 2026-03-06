from .user import router as users_router
from .posts import router as posts_router
from .categories import router as categories_router
from .tags import router as tags_router
from .post_tags import router as post_tags_router
from .post_views import router as post_views_router

__all__ = [
    "users_router",
    "posts_router",
    "categories_router",
    "tags_router",
    "post_tags_router",
    "post_categories_router",
    "post_views_router",
]