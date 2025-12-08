from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base
import uuid
from sqlalchemy.sql import func

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_uuid)
    first_name = Column(String,nullable=True,default="Anonymous")
    last_name = Column(String,nullable=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    tokens = relationship("Token", back_populates="user")
    threads = relationship("Thread", back_populates="user")


class Token(Base):
    __tablename__ = "tokens"
    token = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="tokens")

class Thread(Base):
    __tablename__ = "threads"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="threads")
    messages = relationship("Message", back_populates="thread")

class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, default=generate_uuid)
    thread_id = Column(String, ForeignKey("threads.id"))
    role = Column(String)  # "user" or "assistant"
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    thread = relationship("Thread", back_populates="messages")
