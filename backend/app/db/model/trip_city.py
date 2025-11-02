# app/db/model/trip_city.py
from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, Integer
from datetime import datetime

# 11/2 추가 (나영일): Trip과 City 간의 다대다 관계를 위한 연결 테이블 모델
class TripCity(Base):
    __tablename__ = "trip_cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    start_date: Mapped[datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime] = mapped_column(DateTime)

    trip_id: Mapped[int] = mapped_column(ForeignKey("trip.id"))
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))

    # Trip과의 관계 (N:1)
    trip = relationship("Trip", back_populates="trip_cities")
    # City와의 관계 (N:1)
    city = relationship("City", back_populates="trip_cities")