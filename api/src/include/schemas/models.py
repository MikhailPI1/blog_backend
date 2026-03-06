from pydantic import Field, EmailStr
from typing import Optional, List
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address

from .base import Base


class User(Base):
    """Модель пользователя"""
    id: int
    username: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=255)
    password_hash: str = Field(..., max_length=255)
    avatar_url: Optional[str] = Field(None, max_length=500)
    role: str = Field(default='user', max_length=20)
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None


class UserCreate(Base):
    """Модель для создания пользователя"""
    username: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=255)
    password_hash: str = Field(..., max_length=255)
    bio: Optional[str] = None
    avatar_url: Optional[str] = Field(None, max_length=500)
    role: str = Field(default='user', max_length=20)


class UserUpdate(Base):
    """Модель для обновления пользователя"""
    username: Optional[str] = Field(None, max_length=50)
    bio: Optional[str] = None
    avatar_url: Optional[str] = Field(None, max_length=500)
    role: Optional[str] = Field(None, max_length=20)


class Post(Base):
    """Модель поста"""
    id: int
    slug: str = Field(..., max_length=255)
    title: str = Field(..., max_length=255)
    content: str
    excerpt: Optional[str] = Field(None, max_length=500)
    user_id: int
    views_count: int = Field(default=0, ge=0)
    likes_count: int = Field(default=0, ge=0)
    comments_count: int = Field(default=0, ge=0)
    status: str = Field(default='draft', max_length=20)
    is_featured: bool = False
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None


class PostCreate(Base):
    """Модель для создания поста"""
    slug: str = Field(..., max_length=255)
    title: str = Field(..., max_length=255)
    content: str
    user_id: int
    excerpt: Optional[str] = Field(None, max_length=500)
    status: str = Field(default='draft', max_length=20)
    is_featured: bool = False
    published_at: Optional[datetime] = None


class PostUpdate(Base):
    """Модель для обновления поста"""
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None
    excerpt: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = Field(None, max_length=20)
    is_featured: Optional[bool] = None


class Category(Base):
    """Модель категории"""
    id: int
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=120)
    description: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: int = Field(default=0, ge=0)
    created_at: datetime


class CategoryCreate(Base):
    """Модель для создания категории"""
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=120)
    description: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: int = Field(default=0, ge=0)


class CategoryUpdate(Base):
    """Модель для обновления категории"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: Optional[int] = Field(None, ge=0)


class CategoryWithChildren(Category):
    """Категория с дочерними категориями"""
    children: List['Category'] = []


class Tag(Base):
    """Модель тега"""
    id: int
    name: str = Field(..., max_length=50)
    slug: str = Field(..., max_length=60)
    created_at: datetime


class TagCreate(Base):
    """Модель для создания тега"""
    name: str = Field(..., max_length=50)
    slug: str = Field(..., max_length=60)


class TagUpdate(Base):
    """Модель для обновления тега"""
    name: Optional[str] = Field(None, max_length=50)
    slug: Optional[str] = Field(None, max_length=60)


class PostCategory(Base):
    """Связь поста с категорией"""
    post_id: int
    category_id: int
    created_at: datetime


class PostTag(Base):
    """Связь поста с тегом"""
    post_id: int
    tag_id: int
    created_at: datetime


class PostViewResult(Base):
    """Модель для post_views"""
    id: int
    post_id: int
    user_id: Optional[int] = None
    viewer_ip: Optional[str] = None
    user_agent: Optional[str] = None
    viewed_at: datetime


class PostCategoryResult(Base):
    """Модель для post_categories"""
    post_id: int
    category_id: int
    created_at: datetime
    category: Optional[Category] = None


class PostTagResult(Base):
    """Модель для get_post_tags - возвращает теги поста"""
    tag_id: int
    tag_name: str = Field(..., max_length=50)
    tag_slug: str = Field(..., max_length=60)


class TagPostResult(Base):
    """Модель для get_tag_posts - возвращает посты с тегом"""
    post_id: int
    post_title: str = Field(..., max_length=255)
    post_slug: str = Field(..., max_length=255)
    published_at: Optional[datetime] = None