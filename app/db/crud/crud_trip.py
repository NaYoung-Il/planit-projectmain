from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.db.model.trip import Trip
from app.db.model.trip_day import TripDay
from app.db.model.schedule import Schedule
from app.db.model.checklist_item import ChecklistItem
from app.db.schema.trip import TripCreate, TripUpdate
from app.db.schema.trip_day import TripDayCreate
from app.db.schema.schedule import ScheduleCreate, ScheduleUpdate
from app.db.schema.checklist_item import ChecklistItemCreate, ChecklistItemUpdate

## 1. 여행(Trip) CRUD

# 여행 생성(Create)
async def create_trip(db: AsyncSession, trip: TripCreate) -> Trip:
    db_trip = Trip(**trip.model_dump())
    db.add(db_trip)
    await db.commit()
    await db.refresh(db_trip)
    return db_trip

# 여행 조회(Read)
async def get_trip(db: AsyncSession, trip_id: int) -> Optional[Trip]:
    result = await db.execute(select(Trip).filter(Trip.id == trip_id))
    return result.scalars().first()

# 특정 사용자의 모든 여행 조회(Read)
async def get_trips_by_user(db: AsyncSession, user_id: int) -> List[Trip]:
    result = await db.execute(select(Trip).filter(Trip.user_id == user_id))
    return result.scalars().all()

# 여행 수정(Update)
async def update_trip(db: AsyncSession, trip_id: int, trip_update: TripUpdate) -> Optional[Trip]:
    db_trip = await get_trip(db, trip_id)
    if db_trip:
        # exclude_unset=True 옵션을 사용하여 업데이트할 필드만 적용
        update_data = trip_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_trip, key, value)
        await db.commit()
        await db.refresh(db_trip)
    return db_trip
    
# 여행 삭제(Delete)
async def delete_trip(db: AsyncSession, trip_id: int) -> Optional[Trip]:
    db_trip = await get_trip(db, trip_id)
    if db_trip:
        await db.delete(db_trip)
        await db.commit()
    return db_trip


## 2. 일자별 여행 계획(TripDay) CRUD

# 일자별 여행 계획 생성(Create)
async def create_trip_day(db: AsyncSession, trip_day: TripDayCreate) -> TripDay:
    db_trip_day = TripDay(**trip_day.model_dump())
    db.add(db_trip_day)
    await db.commit()
    await db.refresh(db_trip_day)
    return db_trip_day

# 일자별 여행 계획 조회(Read)
async def get_trip_day(db: AsyncSession, trip_day_id: int) -> Optional[TripDay]:
    result = await db.execute(select(TripDay).filter(TripDay.id == trip_day_id))
    return result.scalars().first()

# 특정 여행의 모든 일자별 여행 계획 조회(Read)
async def get_trip_days_by_trip(db: AsyncSession, trip_id: int) -> List[TripDay]:
    result = await db.execute(select(TripDay).filter(TripDay.trip_id == trip_id))
    return result.scalars().all()

## 3. 세부 일정(Schedule) CRUD

# 세부 일정 생성(Create)
async def create_schedule(db: AsyncSession, schedule: ScheduleCreate) -> Schedule:
    db_schedule = Schedule(**schedule.model_dump())
    db.add(db_schedule)
    await db.commit()
    await db.refresh(db_schedule)
    return db_schedule

# 세부 일정 조회(Read)
async def get_schedule(db: AsyncSession, schedule_id: int) -> Optional[Schedule]:
    result = await db.execute(select(Schedule).filter(Schedule.id == schedule_id))
    return result.scalars().first()

# 특정 일자별 여행 계획의 모든 세부 일정 조회(Read)
async def get_schedules_by_trip_day(db: AsyncSession, trip_day_id: int) -> List[Schedule]:
    result = await db.execute(select(Schedule).filter(Schedule.trip_day_id == trip_day_id))
    return result.scalars().all()

# 세부 일정 수정(Update)
async def update_schedule(db: AsyncSession, schedule_id: int, schedule_update: ScheduleUpdate) -> Optional[Schedule]:
    db_schedule = await get_schedule(db, schedule_id)
    if db_schedule:
        update_data = schedule_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_schedule, key, value)
        await db.commit()
        await db.refresh(db_schedule)
    return db_schedule

# 세부 일정 삭제(Delete)
async def delete_schedule(db: AsyncSession, schedule_id: int) -> Optional[Schedule]:
    db_schedule = await get_schedule(db, schedule_id)
    if db_schedule:
        await db.delete(db_schedule)
        await db.commit()
    return db_schedule


## 4. 준비물 체크리스트(ChecklistItem) CRUD

# 준비물 체크리스트 생성(Create)
async def create_checklist_item(db: AsyncSession, checklist_item: ChecklistItemCreate) -> ChecklistItem:
    db_checklist_item = ChecklistItem(**checklist_item.model_dump())
    db.add(db_checklist_item)
    await db.commit()
    await db.refresh(db_checklist_item)
    return db_checklist_item

# 준비물 체크리스트 조회(Read)
async def get_checklist_item(db: AsyncSession, item_id: int) -> Optional[ChecklistItem]:
    result = await db.execute(select(ChecklistItem).filter(ChecklistItem.id == item_id))
    return result.scalars().first()

# 특정 여행의 모든 준비물 체크리스트 조회(Read)
async def get_checklist_items_by_trip(db: AsyncSession, trip_id: int) -> List[ChecklistItem]:
    result = await db.execute(select(ChecklistItem).filter(ChecklistItem.trip_id == trip_id))
    return result.scalars().all()

# 준비물 체크리스트 수정(Update)
async def update_checklist_item(db: AsyncSession, item_id: int, item_update: ChecklistItemUpdate) -> Optional[ChecklistItem]:
    db_checklist_item = await get_checklist_item(db, item_id)
    if db_checklist_item:
        update_data = item_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_checklist_item, key, value)
        await db.commit()
        await db.refresh(db_checklist_item)
    return db_checklist_item

# 준비물 체크리스트 삭제(Delete)
async def delete_checklist_item(db: AsyncSession, item_id: int) -> Optional[ChecklistItem]:
    db_checklist_item = await get_checklist_item(db, item_id)
    if db_checklist_item:
        await db.delete(db_checklist_item)
        await db.commit()
    return db_checklist_item