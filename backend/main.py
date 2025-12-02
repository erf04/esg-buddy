
from db.base import Base, engine
from routes.auth import router as auth_router
from fastapi import FastAPI
from routes.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)   # optional
        await conn.run_sync(Base.metadata.create_all)

    yield   # Application runs here

    # Shutdown logic (optional)
    # e.g., closing resources


app = FastAPI(title="ESG Buddy Backend with ORM",lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)


if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True)