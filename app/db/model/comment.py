from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger,String, Text, TIMESTAMP, func, ForeignKey
from ..database import Base
from typing import Optional, List
from datetime import datetime

class Comment(Base):
    __tablename__ = 'comments'

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    review_id:Mapped[int] = mapped_column(ForeignKey("review.id", ondelete="CASCADE"), nullable=False)
    content:Mapped[str] = mapped_column(Text)
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now())

# # FOREIGN KEY (user_id) REFERENCES users(id) on delete cascade,
    users = relationship("User", back_populates="comments", lazy="selectin")
# # FOREIGN KEY (review_id) REFERENCES review(id) on delete cascade
    review = relationship("Review", back_populates="comments", lazy="selectin")