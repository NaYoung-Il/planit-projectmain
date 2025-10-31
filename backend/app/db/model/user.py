# app/db/models/user.py
from sqlalchemy import Column, Integer, String,ForeignKey
from app.db.database import Base # Base는 declarative_base()로 정의된 클래스라고 가정
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True,  nullable=False)
    password = Column(String(   255), nullable=False) 
    group_id = Column(
        Integer,
        ForeignKey("GROUPT.id"), 
        nullable=False,
        default=1 #1이 일반 사용자라는 가장하에 작성
    )

    group = relationship("Group", back_populates="users")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    #trip/review relationship 추가
    trip = relationship("Trip", back_populates="users", cascade="all, delete-orphan")
    review = relationship("Review", back_populates="users", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="users", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="users")