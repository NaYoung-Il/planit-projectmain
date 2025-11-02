from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger, ForeignKey
from typing import Optional

class ChecklistItem(Base):
    __tablename__ = "checklist_item"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True) 
    trip_id: Mapped[Optional[int]] = mapped_column(ForeignKey("trip.id"), nullable=True)  # 수정됨 : trip_day에서 trip으로 연결 수정 
    item_name: Mapped[str] = mapped_column(String(255), nullable=False)  
    is_checked: Mapped[bool] = mapped_column(nullable=False, default=False)  

    trip = relationship("Trip", back_populates="checklist_item")

# CREATE TABLE checklist_item (
#     id BIGINT PRIMARY KEY AUTO_INCREMENT,
#     trip_id BIGINT,                         -- 수정됨 : trip_day에서 trip으로 연결 수정 
#     item_name VARCHAR(255) NOT NULL,
#     is_checked BOOLEAN DEFAULT FALSE,
#     FOREIGN KEY (trip_id) REFERENCES trip(id) on delete cascade
# );