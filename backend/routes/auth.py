from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from db.models import User, Token
from db.base import get_session
from services.auth import hash_password, verify_password
import secrets
from schemas import auth as auth_schema
from schemas.user import UserOut

router = APIRouter(prefix="/auth", tags=["Auth"])



@router.post("/register")
async def register(data: auth_schema.RegisterIn, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    print("user password",data.password)
    user = User(
        first_name = data.first_name,
        last_name=data.last_name,
        email=data.email,
        hashed_password=hash_password(data.password)
    )
    db.add(user)
    await db.commit()
    return {"message": "User registered successfully"}


@router.post("/login")
async def login(data: auth_schema.LoginIn, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate a simple persistent token
    token_str = secrets.token_hex(32)
    token = Token(token=token_str, user_id=user.id)
    db.add(token)
    await db.commit()

    return auth_schema.LoginOut(token=token_str,user=UserOut.model_validate(user))

    # return {"token": token_str,"user":{"id":user.id,"first_name":user.first_name}}
