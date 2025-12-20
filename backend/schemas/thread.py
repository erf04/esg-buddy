from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime
from message import MessageOut


class ThreadSummary(BaseModel):
    thread_id: str
    created_at: datetime
    message_count: int
    last_message: Optional[str] = None
    last_message_time: Optional[datetime] = None
    has_pdfs: bool = False
    
    class Config:
        from_attributes = True

class ThreadDetail(ThreadSummary):
    messages: List[MessageOut]
    has_pdfs: bool = False