from fastapi import APIRouter, Depends, HTTPException, logger, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import json
from fastapi.responses import StreamingResponse
from datetime import datetime
import io
from typing import Optional
from sqlalchemy import desc

from db.base import get_session
from db.models import Thread, User, Message
from schemas.message import MessageIn, MessageOut
from services.openai_service import OpenAIService
from services.auth import get_current_user
from services.pdf import markdown_to_pdf
import logging 


router = APIRouter(prefix="/chat", tags=["Chat"])

openai_service = OpenAIService()

logger = logging.getLogger(__name__)

@router.post("/stream")
async def stream_message(payload: MessageIn,
                         db: AsyncSession = Depends(get_session),
                         user: User = Depends(get_current_user)):
    print("Streaming message received:", payload.content)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not payload.content or payload.content.strip() == "":
        raise HTTPException(status_code=400, detail="Message content cannot be empty")
    
    thread_id = payload.thread_id
    # If thread_id is provided, use it, otherwise find existing thread
    if thread_id:
        # Verify the thread belongs to the user
        result = await db.execute(
            select(Thread).where(Thread.id == thread_id, Thread.user_id == user.id)
        )
        thread = result.scalar_one_or_none()
        
        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")
        thread_id = thread.id
    else:
        # Find or create thread
        result = await db.execute(
            select(Thread).where(Thread.user_id == user.id)
            .order_by(desc(Thread.created_at))
            .limit(1)
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
            rate_limit_detected = False
            empty_response = True
            
            async for token in openai_service.stream_response(thread_id, payload.content):
                if token:
                    # Check for rate limit error in token
                    if token.startswith("[RATE_LIMIT_ERROR]"):
                        rate_limit_detected = True
                        error_msg = token.replace("[RATE_LIMIT_ERROR]", "").strip()
                        yield f"data: {json.dumps({'error': error_msg, 'type': 'rate_limit'})}\n\n"
                        break
                    elif token.startswith("[ERROR]"):
                        error_msg = token.replace("[ERROR]", "").strip()
                        yield f"data: {json.dumps({'error': error_msg, 'type': 'general'})}\n\n"
                        break
                    else:
                        empty_response = False
                        full_response += token
                        yield f"data: {json.dumps({'delta': token})}\n\n"
            
            # Save assistant response to database if we got content
            if full_response and not rate_limit_detected:
                assistant_msg = Message(
                    thread_id=thread_id, 
                    role="assistant", 
                    content=full_response
                )
                db.add(assistant_msg)
                await db.commit()
            
            # Check for empty response
            if empty_response and not rate_limit_detected:
                yield f"data: {json.dumps({'error': 'Empty response from assistant', 'type': 'empty_response'})}\n\n"
            
            yield f"data: {json.dumps({'done': True})}\n\n"
            
        except Exception as e:
            error_str = str(e)
            logger.error(f"Streaming error: {error_str}")
            
            # Check for rate limit in error
            if "rate_limit" in error_str.lower() or "429" in error_str:
                yield f"data: {json.dumps({'error': error_str, 'type': 'rate_limit'})}\n\n"
            else:
                yield f"data: {json.dumps({'error': error_str, 'type': 'general'})}\n\n"
            
            yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(
        event_generator(), 
        media_type="text/event-stream",
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'
        }
    )


@router.get("/{thread_id}/messages")
async def get_thread_messages(
    thread_id: str,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """
    Get all messages for a specific thread
    """
    try:
        # Verify the thread belongs to the user
        result = await db.execute(
            select(Thread)
            .where(Thread.id == thread_id, Thread.user_id == user.id)
            .options(selectinload(Thread.messages))
        )
        thread = result.scalar_one_or_none()
        
        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")
        
        # Sort messages by creation time
        messages = sorted(thread.messages, key=lambda m: m.created_at)
        
        # Format response
        formatted_messages = []
        for message in messages:
            msg_dict = {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at.isoformat(),
                "has_pdf": message.has_pdf,
            }
            
            if message.has_pdf:
                msg_dict.update({
                    "pdf_filename": message.pdf_filename,
                    "pdf_size": message.pdf_size,
                    "pdf_download_url": f"/chat/download-pdf/{message.id}"
                })
            
            formatted_messages.append(msg_dict)
        
        # Get thread info
        has_pdfs = any(msg.has_pdf for msg in thread.messages)
        
        return {
            "thread_id": thread.id,
            "created_at": thread.created_at.isoformat(),
            "message_count": len(messages),
            "has_pdfs": has_pdfs,
            "messages": formatted_messages
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch thread messages: {str(e)}")


@router.get("/generate-esg-report")
async def generate_esg_report(
    thread_id: str,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """
    Simple endpoint to generate ESG report from conversation
    """
    try:
        # 1. Get user's thread
        result = await db.execute(
            select(Thread).where(Thread.id == thread_id, Thread.user_id == user.id)
        )
        thread = result.scalar_one_or_none()
        
        if not thread:
            raise HTTPException(status_code=400, detail="No conversation found. Please chat first.")
        
        # 2. Get ESG report text from AI
        try:
            report_text = await openai_service.generate_esg_report_text(thread.id)
            
            # Check for empty response
            if not report_text or report_text.strip() == "":
                raise HTTPException(status_code=400, detail="Empty response from AI. This conversation may be too long.")
                
        except Exception as e:
            error_str = str(e)
            logger.error(f"Error in ESG report generation: {error_str}")
            
            # Check for rate limit
            if "rate_limit" in error_str.lower():
                raise HTTPException(
                    status_code=429,
                    detail="This conversation has reached its token limit. Please start a new conversation to continue."
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to generate ESG report: {error_str}"
                )
        
        # 3. Convert text to PDF
        pdf_bytes = markdown_to_pdf(report_text)
        
        # 4. Save user's "Generate ESG Report" message
        user_msg = Message(
            thread_id=thread.id,
            role="user",
            content="Please generate an ESG report based on our conversation"
        )
        db.add(user_msg)
        
        # 5. Save assistant's response WITH PDF attachment
        filename = f"ESG_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        assistant_msg = Message(
            thread_id=thread.id,
            role="assistant",
            content="I've analyzed our conversation and generated an ESG report. You can download it below.",
            has_pdf=True,
            pdf_filename=filename,
            pdf_data=pdf_bytes,
            pdf_size=len(pdf_bytes)
        )
        db.add(assistant_msg)
        
        await db.commit()
        await db.refresh(assistant_msg)
        
        # 6. Return success with message info
        return {
            "success": True,
            "message": "ESG report generated successfully",
            "message_id": assistant_msg.id,
            "has_pdf": True,
            "pdf_filename": filename,
            "pdf_size": len(pdf_bytes),
            "created_at": assistant_msg.created_at.isoformat()
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Failed to generate ESG report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate ESG report: {str(e)}")


@router.get("/download-pdf/{message_id}/")
async def download_pdf(
    message_id: str,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """
    Download PDF attached to a message
    """
    # Get the message with PDF
    result = await db.execute(
        select(Message)
        .join(Thread)
        .where(
            Message.id == message_id,
            Thread.user_id == user.id,
            Message.has_pdf == True
        )
    )
    message = result.scalar_one_or_none()
    
    if not message or not message.pdf_data:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    # Return PDF file
    return StreamingResponse(
        io.BytesIO(message.pdf_data),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={message.pdf_filename}",
            "Content-Length": str(message.pdf_size)
        }
    )