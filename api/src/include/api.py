from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import user, posts, categories, tags, post_tags, post_views


app = FastAPI(
    title="Blog API",
    description="API для управления блогом",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api/users", tags=["Users"])
app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(tags.router, prefix="/api/tags", tags=["Tags"])
app.include_router(post_tags.router, prefix="/api/post-tags", tags=["Post Tags"])
app.include_router(post_views.router, prefix="/api/post-views", tags=["Post Views"])
