from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import List, Optional
from app.db.schema.trip_city import TripCityCreate, TripCityUpdate, TripCityInDB
from app.db.schema.trip_day import TripDayInDB

# 11/2 수정 (나영일): city_id 대신 '도시 박스' 배열을 받는다.
# 이 필드는 Trip 생성/수정 시 항상 필요하다.
class TripBase(BaseModel):
    title: str = Field(..., max_length=100)
    start_date: date
    end_date: Optional[date] = None

class TripCreate(TripBase):
    user_id: int     
    trip_cities: List[TripCityCreate]

class TripUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    trip_cities: Optional[List[TripCityUpdate]] = None

class TripInDB(TripBase):
    id: int
    user_id: int
    trip_cities: List[TripCityInDB] = []

    class Config:
        from_attributes = True