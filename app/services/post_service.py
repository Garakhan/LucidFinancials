# app/services/post_service.py
from app.models.post import Post
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.cache import get_from_cache, set_cache, invalidate_cache

async def add_post(user_id: int, text: str, session: AsyncSession):
    """Add a new post for the authenticated user and invalidate cache."""
    post = Post(text=text, user_id=user_id)
    session.add(post)
    await session.commit()
    invalidate_cache(user_id)  # Refresh cache after change
    return post.id

async def get_user_posts(user_id: int, session: AsyncSession):
    """Return posts for the user from cache if available, otherwise fetch from DB."""
    posts = get_from_cache(user_id)
    if posts:
        return posts

    result = await session.execute(select(Post).filter_by(user_id=user_id))
    posts = result.scalars().all()
    set_cache(user_id, posts)
    return posts

async def delete_post(user_id: int, post_id: int, session: AsyncSession):
    """Delete the specified post and invalidate user's cache."""
    result = await session.execute(select(Post).filter_by(id=post_id, user_id=user_id))
    post = result.scalars().first()
    if post:
        await session.delete(post)
        await session.commit()
        invalidate_cache(user_id)