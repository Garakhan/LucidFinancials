# app/services/auth_service.py
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.core.jwt_handler import create_access_token


def hash_password(password: str) -> str:
    """Hash the password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(plain: str, hashed: str) -> bool:
    """Verify the password against the hashed value."""
    return bcrypt.checkpw(plain.encode(), hashed.encode())


async def signup_user(email: str, password: str, session: AsyncSession):
    """Sign up a new user and return JWT token."""
    result = await session.execute(select(User).filter_by(email=email))
    if result.scalars().first():
        raise ValueError("User already exists")
    user = User(email=email, hashed_password=hash_password(password))
    session.add(user)
    await session.commit()
    return create_access_token({"sub": user.id})


async def login_user(email: str, password: str, session: AsyncSession):
    """Login a user and return JWT token."""
    result = await session.execute(select(User).filter_by(email=email))
    user = result.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        raise ValueError("Invalid credentials")
    return create_access_token({"sub": user.id})