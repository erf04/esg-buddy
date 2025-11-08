from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from db.base import get_session
from db.models import Thread, User,Message
from schemas.message import MessageIn, MessageOut
from services.openai_service import OpenAIService
from services.auth import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])


openai_service = OpenAIService()

@router.post("/send-message")
async def send_message(payload: MessageIn,
                        db: AsyncSession = Depends(get_session),
                        user: User = Depends(get_current_user)
                        ):
    # 🔹 Find or create user
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 🔹 Find existing thread or create new one
    result = await db.execute(
        select(Thread).where(Thread.user_id == user.id).limit(1)
    )
    thread = result.scalar_one_or_none()

    if not thread:
        thread_id = await openai_service.create_thread()
        thread = Thread(id=thread_id, user_id=user.id)
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
    # return {}
    return MessageOut(role="assistant", content=reply_text, thread_id=thread_id, created_at=assistant_msg.created_at.isoformat())


@router.get("/messages/{user_id}")
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
