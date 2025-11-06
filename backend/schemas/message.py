from pydantic import BaseModel


# Pydantic schema
class MessageIn(BaseModel):
    user_id: str
    content: str

class MessageOut(BaseModel):
    role: str
    content: str
    thread_id: str
    created_at: str