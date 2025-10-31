from pydantic import BaseModel
from datetime import date

class TripDayBase(BaseModel):
    day_date: date
    day_sequence: int  # n일차 표시용

class TripDayCreate(TripDayBase):
    trip_id: int

class TripDayInDB(TripDayBase):
    id: int
    trip_id: int

    class Config:
        from_attributes = True