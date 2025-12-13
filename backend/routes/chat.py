from fastapi import APIRouter, Depends, HTTPException, logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from db.base import get_session
from db.models import Thread, User,Message
from schemas.message import MessageIn, MessageOut
from services.openai_service import OpenAIService
from services.auth import get_current_user
from services.pdf import markdown_to_pdf
import json
from fastapi.responses import StreamingResponse
from datetime import datetime
import io
from services.pdf import html



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
    print(payload.content)
    if payload.content == None or payload.content.strip() == "":
        raise HTTPException(status_code=400, detail="payload is not ok")
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


@router.post("/stream")
async def stream_message(payload: MessageIn,
                         db: AsyncSession = Depends(get_session),
                         user: User = Depends(get_current_user)):
    print("Streaming message received:", payload.content)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not payload.content or payload.content.strip() == "":
        raise HTTPException(status_code=400, detail="Message content cannot be empty")

    # Find or create thread
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

    # Save user message
    user_msg = Message(thread_id=thread_id, role="user", content=payload.content)
    db.add(user_msg)
    await db.commit()

    async def event_generator():
        try:
            full_response = ""
            async for token in openai_service.stream_response(thread_id, payload.content):
                if token:
                    # print("Streaming token:", token)
                    full_response += token
                    yield f"data: {json.dumps({'delta': token})}\n\n"
            
            # Save assistant response to database
            if full_response:
                assistant_msg = Message(
                    thread_id=thread_id, 
                    role="assistant", 
                    content=full_response
                )
                db.add(assistant_msg)
                await db.commit()
                
            yield f"data: {json.dumps({'done': True})}\n\n"
            
        except Exception as e:
            logger.error(f"Streaming error: {str(e)}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(
        event_generator(), 
        media_type="text/event-stream",
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'  # Important for nginx
        }
    )


@router.get("/messages/")
async def get_messages(db: AsyncSession = Depends(get_session),
                       user:User = Depends(get_current_user)):
    # 🔹 Find user and load messages with thread relationship
    result = await db.execute(
        select(Thread)
        .options(selectinload(Thread.messages))
        .where(Thread.user_id == user.id)
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



@router.get("/generate-esg-pdf")
async def generate_esg_pdf(
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """
    Simple endpoint to generate ESG PDF from conversation
    """
    try:
        # 1. Get user's thread
        result = await db.execute(
            select(Thread).where(Thread.user_id == user.id).limit(1)
        )
        thread = result.scalar_one_or_none()
        
        if not thread:
            raise HTTPException(status_code=400, detail="No conversation found. Please chat first.")
        
        # 2. Get ESG report text from AI
        # report_text = await openai_service.generate_esg_report_text(thread.id)
        
        # 3. Convert text to PDF
        # pdf_generator = SimplePDFGenerator()
        # pdf_bytes = pdf_generator.text_to_pdf(report_text, "ESG Sustainability Report")
        pdf_bytes = markdown_to_pdf(html)
        # 4. Create a simple user message in chat
        # user_msg = Message(
        #     thread_id=thread.id,
        #     role="user",
        #     content="Generate ESG report"
        # )
        # db.add(user_msg)
        
        # 5. Create assistant message with PDF info
        # filename = f"ESG_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        # assistant_msg = Message(
        #     thread_id=thread.id,
        #     role="assistant",
        #     content=f"I've generated an ESG report based on our conversation. You can download it here."
        # )
        # db.add(assistant_msg)
        # await db.commit()
        
        # 6. Return PDF as downloadable file
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=mmd",
                "Content-Type": "application/pdf"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")
