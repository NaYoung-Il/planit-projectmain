from pydantic import BaseModel
from datetime import time, datetime
from typing import Optional

class ScheduleBase(BaseModel):
    schedule_content: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

class ScheduleCreate(ScheduleBase):
    trip_day_id: int
    place_id: Optional[int] = None # 장소는 선택사항
    schedule_datetime: datetime # 일정 생성 시점 기록용

class ScheduleUpdate(BaseModel):
    schedule_content: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    place_id: Optional[int] = None

class ScheduleInDB(ScheduleBase):
    id: int
    trip_day_id: int
    place_id: Optional[int] = None
    schedule_datetime: datetime

    class Config:
        from_attributes = True