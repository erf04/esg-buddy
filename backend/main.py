from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from db.base import Base, engine, get_session
from db.models import User, Thread, Message
from services.openai_service import OpenAIService
from schemas.message import MessageIn,MessageOut


app = FastAPI(title="ESG Buddy Backend with ORM")
openai_service = OpenAIService()




@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/send-message")
async def send_message(payload: MessageIn, db: AsyncSession = Depends(get_session)) -> MessageOut:
    # 🔹 Find or create user
    user = await db.get(User, payload.user_id)
    if not user:
        user = User(id=payload.user_id, email="Anonymous@gmail.com")
        db.add(user)
        await db.commit()

    # 🔹 Find existing thread or create new one
    result = await db.execute(
        select(Thread).where(Thread.user_id == payload.user_id).limit(1)
    )
    thread = result.scalar_one_or_none()

    if not thread:
        thread_id = await openai_service.create_thread()
        thread = Thread(id=thread_id, user_id=payload.user_id)
        db.add(thread)
        await db.commit()
    else:
        thread_id = thread.id

    # 🔹 Save user message
    user_msg = Message(thread_id=thread_id, role="user", content=payload.content)
    db.add(user_msg)
    await db.commit()

    # 🔹 Get response from assistant
    reply_text = await openai_service.send_message(thread_id, payload.content)

    # 🔹 Save assistant message
    assistant_msg = Message(thread_id=thread_id, role="assistant", content=reply_text)
    db.add(assistant_msg)
    await db.commit()
    return MessageOut(role="assistant", content=reply_text, thread_id=thread_id, created_at=assistant_msg.created_at.isoformat())


@app.get("/messages/{user_id}")
async def get_messages(user_id: str, db: AsyncSession = Depends(get_session)):
    # 🔹 Find user and load messages with thread relationship
    result = await db.execute(
        select(Thread)
        .options(selectinload(Thread.messages))
        .where(Thread.user_id == user_id)
    )
    thread = result.scalar_one_or_none()

    if not thread:
        raise HTTPException(status_code=404, detail="No thread found for this user")

    # 🔹 Order messages by time
    messages = sorted(thread.messages, key=lambda m: m.created_at)

    return [
        {"role": m.role, "content": m.content, "created_at": m.created_at.isoformat()}
        for m in messages
    ]
