from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger,String, Text, TIMESTAMP, func, ForeignKey
from ..database import Base
from typing import Optional, List
from datetime import datetime


class Review(Base):
    __tablename__ ='review'

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    trip_id:Mapped[int] = mapped_column(ForeignKey("trip.id", ondelete="CASCADE"), nullable=False)
    title:Mapped[str] = mapped_column(String(255),nullable=False)
    content:Mapped[str] = mapped_column(Text, nullable=False)
    rating:Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now())
    
    users = relationship("User", back_populates="review", lazy="selectin")  #     
    trip = relationship("Trip", back_populates="review", lazy="selectin") 
    comments = relationship("Comment", back_populates="review", lazy="selectin", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="review", cascade="all, delete-orphan")
    photos = relationship("Photo", back_populates="review", lazy="selectin", cascade="all, delete-orphan")

#like
class Like(Base):
    __tablename__ ='likes'
    # primary key(user_id,review_id) 복합키 - 좋아요 중복방지
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    review_id:Mapped[int]= mapped_column(ForeignKey("review.id", ondelete="CASCADE"), primary_key=True ,nullable=False)
    
    users = relationship("User", back_populates="likes")     
    review = relationship("Review", back_populates="likes")
        

    