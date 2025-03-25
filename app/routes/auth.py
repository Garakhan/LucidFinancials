from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.database import get_session
from app.services.auth_service import signup_user, login_user

router = APIRouter()

@router.post("/signup", response_model=Token)
async def signup(data: UserCreate, session: AsyncSession = Depends(get_session)):
    """Signup endpoint."""
    try:
        token = await signup_user(data.email, data.password, session)
        return {"access_token": token}
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/login", response_model=Token)
async def login(data: UserLogin, session: AsyncSession = Depends(get_session)):
    """Login endpoint."""
    try:
        token = await login_user(data.email, data.password, session)
        return {"access_token": token}
    except ValueError as e:
        raise HTTPException(401, str(e))