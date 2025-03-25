# app/routes/post.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.dependencies.auth import get_current_user
from app.schemas.post import PostCreate, PostResponse
from app.services.post_service import add_post, get_user_posts, delete_post

router = APIRouter()

@router.post("/add")
async def create_post(
    data: PostCreate,
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)):
    """Add post endpoint."""
    if len(data.text.encode()) > 1_000_000:
        raise HTTPException(400, "Payload exceeds 1MB")
    post_id = await add_post(user_id, data.text, session)
    return {"postID": post_id}

@router.get("/all", response_model=list[PostResponse])
async def get_posts(
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)):
    """Get posts endpoint."""
    posts = await get_user_posts(user_id, session)
    return posts

@router.delete("/delete/{post_id}")
async def delete_user_post(
    post_id: int,
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)):
    """Delete post endpoint."""
    await delete_post(user_id, post_id, session)
    return {"message": "Post deleted"}
