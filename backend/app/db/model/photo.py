from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger,String, Text, TIMESTAMP, func, ForeignKey
from sqlalchemy.dialects.mysql import LONGBLOB
from ..database import Base
from datetime import datetime
from typing import Optional

class Photo(Base):
    __tablename__ ='photos'

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    review_id:Mapped[int] = mapped_column(ForeignKey("review.id", ondelete="CASCADE"), nullable=False) #
    filename:Mapped[str] = mapped_column(String(255),nullable=False)
    data:Mapped[bytes] = mapped_column(LONGBLOB,nullable=False)
    content_type:Mapped[str] =mapped_column(String(50),nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now()) 
    
    # FOREIGN KEY (review_id) REFERENCES review(id) ON DELETE CASCADE
    review = relationship("Review", back_populates="photos",lazy='selectin')