
from db.base import Base, engine, get_session
from db.models import User, Thread, Message
from services.openai_service import OpenAIService
from schemas.message import MessageIn,MessageOut
from routes.auth import router as auth_router
from fastapi import FastAPI
from routes.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ESG Buddy Backend with ORM")


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # # Drop all tables first
        # await conn.run_sync(Base.metadata.drop_all)
        # Then recreate them
        await conn.run_sync(Base.metadata.create_all)
