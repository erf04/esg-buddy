import secrets
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from db.base import get_session
from db.models import User, Token
from sqlalchemy.orm import selectinload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



async def get_current_user(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_session)
) -> User:
    """Extracts Bearer token from headers, validates it, and returns the User."""

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    token_str = authorization.split(" ")[1]
    result = await db.execute(
        select(Token)
        .where(Token.token == token_str)
        .options(selectinload(Token.user))
    )
    token_obj = result.scalar_one_or_none()

    if not token_obj or not token_obj.user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return token_obj.user