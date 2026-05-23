"""
Database module for Secret Chat Bot
Defines SQLAlchemy models
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from config import DATABASE_URL

# Create database engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(20), unique=True, nullable=False)
    username = Column(String(255), unique=True, nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    encryption_key = Column(Text, nullable=False)
    password_hash = Column(Text, nullable=True)
    password_salt = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    chats = relationship("Chat", secondary="chat_members", back_populates="members")
    messages = relationship("Message", back_populates="sender")
    
    def __repr__(self):
        return f"<User {self.username or self.telegram_id}>"


class Chat(Base):
    """Secret Chat model"""
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True)
    chat_code = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    encryption_key = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    members = relationship("User", secondary="chat_members", back_populates="chats")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Chat {self.chat_code}>"


class ChatMember(Base):
    """Chat Members association table"""
    __tablename__ = "chat_members"
    
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)


class Message(Base):
    """Encrypted Message model"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    encrypted_content = Column(Text, nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", back_populates="messages")
    
    def __repr__(self):
        return f"<Message {self.id} in Chat {self.chat_id}>"


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")


def get_session():
    """Get a new database session"""
    return Session()
