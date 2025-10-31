from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey
from datetime import datetime

class TripDay(Base):
    __tablename__ = "trip_day"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True) 
    trip_id: Mapped[int] = mapped_column(ForeignKey("trip.id"), nullable=False) 
    day_date: Mapped[datetime] = mapped_column(nullable=False)  
    day_sequence: Mapped[int] = mapped_column(nullable=False)  # n일차 표시용

    trip = relationship("Trip", back_populates="trip_day")
    schedule = relationship("Schedule", back_populates="trip_day")

# CREATE TABLE trip_day (
#     id BIGINT PRIMARY KEY AUTO_INCREMENT,
#     trip_id BIGINT NOT NULL,
#     day_date DATE NOT NULL,
#     day_sequence INT NOT NULL, -- 1일차, 2일차    
#     FOREIGN KEY (trip_id) REFERENCES trip(id) ON DELETE CASCADE
# );
