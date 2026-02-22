from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# load_dotenv()

DATABASE_URL = f"postgresql+asyncpg://{os.getenv('DB_USER','postgres')}:{os.getenv('DB_PASSWORD','koala04')}@{os.getenv('DB_HOST','localhost')}:5432/{os.getenv('DB_NAME','esgbuddy')}"
engine = create_async_engine(DATABASE_URL, echo=False)

async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

from db import models

async def get_session():
    async with async_session() as session:
        yield session
