from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger, ForeignKey
from datetime import datetime
from typing import Optional

class Trip(Base):
    __tablename__ = "trip"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True) 
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False) 
    title: Mapped[str] = mapped_column(String(100), nullable=False)  
    start_date: Mapped[datetime] = mapped_column(nullable=False)  
    end_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)  

    users = relationship("User", back_populates="trip")
    city = relationship("City", back_populates="trip",lazy="selectin")
    trip_day = relationship("TripDay", back_populates="trip", cascade="all, delete-orphan")
    checklist_item = relationship("ChecklistItem", back_populates="trip", cascade="all, delete-orphan")
    review = relationship("Review", back_populates="trip") # cascade="all, delete" orm level

# CREATE TABLE trip (
#     id BIGINT PRIMARY KEY AUTO_INCREMENT,
#     user_id BIGINT NOT NULL,
#     city_id BIGINT NOT NULL,                  -- FK 추가: trip과 도시 연결
#     title VARCHAR(100) NOT NULL,              -- 변경됨: 수정본은 city_name, 초본 스타일에 맞춰 title로 통일    
#     start_date DATETIME NOT NULL,             -- 변경됨: 수정본은 trip_start, 초본은 start_date
#     end_date DATETIME,                        -- 변경됨: 수정본은 trip_end, 초본은 end_date
#     FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
#     FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
# );