from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional
from app.db.schema.city import CityInDB

# 11/2 추가 (나영일): TripCity 관련 스키마
class TripCityBase(BaseModel):
    start_date: date
    end_date: date
    city_id: int

class TripCityCreate(TripCityBase):
    pass

class TripCityUpdate(TripCityBase):
    pass

class TripCityInDB(TripCityBase):
    id: int
    trip_id: int
    city: CityInDB  # City 정보 포함

    class Config:
        from_attributes = True
