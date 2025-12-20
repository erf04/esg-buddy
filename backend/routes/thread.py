
from fastapi import APIRouter, Depends, HTTPException, logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from db.base import get_session
from db.models import Thread, User
from services.auth import get_current_user
from datetime import datetime
from sqlalchemy import desc
from typing import List, Optional
from services.openai_service import OpenAIService

router = APIRouter(prefix="/threads", tags=["Chat"])

openai_service = OpenAIService()

@router.get("/")
async def get_user_threads(
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """
    Get all threads for the current user with summaries
    """
    try:
        # Get all threads for the user
        result = await db.execute(
            select(Thread)
            .where(Thread.user_id == user.id)
            .order_by(desc(Thread.created_at))
            .options(selectinload(Thread.messages))
        )
        threads = result.scalars().all()
        
        thread_summaries = []
        for thread in threads:
            # Get message count and last message
            message_count = len(thread.messages)
            last_message = None
            last_message_time = None
            has_pdfs = False
            
            if thread.messages:
                # Sort messages by creation time
                sorted_messages:List = sorted(thread.messages, key=lambda m: m.created_at, reverse=True)
                last_message = sorted_messages[0].content[:100] + "..." if len(sorted_messages[0].content) > 100 else sorted_messages[0].content
                last_message_time = sorted_messages[0].created_at
                
                # Check if any message has PDF
                has_pdfs = any(msg.has_pdf for msg in thread.messages)
            
            thread_summaries.append({
                "thread_id": thread.id,
                "created_at": thread.created_at,
                "message_count": message_count,
                "last_message": last_message,
                "last_message_time": last_message_time,
                "has_pdfs": has_pdfs,
                "thread_title": f"Conversation {datetime.strftime(thread.created_at, '%b %d')}" if thread.created_at else "New Conversation"
            })
        
        return thread_summaries
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch threads: {str(e)}")
    


@router.post("/new")
async def create_new_thread(
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """
    Create a new empty thread for the user
    """
    try:
        # Create a new thread in OpenAI
        thread_id = await openai_service.create_thread()
        
        # Save to database
        new_thread = Thread(
            id=thread_id,
            user_id=user.id,
            created_at=datetime.utcnow()
        )
        db.add(new_thread)
        await db.commit()
        
        return {
            "success": True,
            "thread_id": thread_id,
            "message": "New conversation created"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create new thread: {str(e)}")

@router.delete("/{thread_id}")
async def delete_thread(
    thread_id: str,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """
    Delete a thread and all its messages
    """
    try:
        # Verify the thread belongs to the user
        result = await db.execute(
            select(Thread)
            .where(Thread.id == thread_id, Thread.user_id == user.id)
        )
        thread = result.scalar_one_or_none()
        
        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")
        
        # Delete thread (cascade will delete messages)
        await db.delete(thread)
        await db.commit()
        
        return {
            "success": True,
            "message": "Conversation deleted successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete thread: {str(e)}")