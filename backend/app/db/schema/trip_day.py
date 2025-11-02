from pydantic import BaseModel
from datetime import date

# 11/2 수정(나영일): day_date(절대 날짜) 필드 삭제
class TripDayBase(BaseModel):
    day_sequence: int  # n일차 표시용

class TripDayCreate(TripDayBase):
    trip_id: int

class TripDayInDB(TripDayBase):
    id: int
    trip_id: int

    class Config:
        from_attributes = True