from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TripBase(BaseModel):
    title: str = Field(..., max_length=100)
    start_date: datetime
    end_date: Optional[datetime] = None

class TripCreate(TripBase):
    user_id: int     
    city_id: int

class TripUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    city_id: Optional[int] = None

class TripInDB(TripBase):
    id: int
    user_id: int
    city_id: int

    class Config:
        from_attributes = True