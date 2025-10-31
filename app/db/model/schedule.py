from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger, Time, ForeignKey
from datetime import datetime, time
from typing import Optional

class Schedule(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True) 
    trip_day_id: Mapped[Optional[int]] = mapped_column(ForeignKey("trip_day.id"), nullable=True)  
    place_id: Mapped[Optional[int]] = mapped_column(ForeignKey("places.id"), nullable=True)  
    schedule_content: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  
    start_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)  
    end_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)  
    schedule_datetime: Mapped[datetime] = mapped_column(nullable=False)  

    trip_day = relationship("TripDay", back_populates="schedule")
    place = relationship("Place", back_populates="schedule")

# CREATE TABLE schedule (
#     id BIGINT PRIMARY KEY AUTO_INCREMENT,
#     trip_day_id BIGINT,                     
#     place_id BIGINT,						  -- 추가됨: places 테이블을 참조하는 FK 추가
#     schedule_content TEXT,                  -- 추가됨: 수정본에서만 존재
#     start_time TIME,                        
#     end_time TIME,                          
#     schedule_datetime DATETIME NOT NULL,    -- 추가됨: 수정본 date
#     FOREIGN KEY (trip_day_id) REFERENCES trip_day(id) ON DELETE CASCADE,
#     FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE SET NULL
# );