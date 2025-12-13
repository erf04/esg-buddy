from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Pydantic schema
class MessageIn(BaseModel):
    content: str

class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    has_pdf: bool = False
    pdf_filename: Optional[str] = None
    pdf_size: Optional[int] = None
    pdf_download_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True