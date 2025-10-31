from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.services.trip_service import TripService
from app.db.schema.trip import TripCreate, TripUpdate, TripInDB
from app.db.schema.trip_day import TripDayCreate, TripDayInDB
from app.db.schema.schedule import ScheduleCreate, ScheduleUpdate, ScheduleInDB
from app.db.schema.checklist_item import ChecklistItemCreate, ChecklistItemUpdate, ChecklistItemInDB

trip_service = TripService()

router = APIRouter(prefix="/trips", tags=["Trips"])

# 1. 여행(Trip) 관련 API 엔드포인트

# 여행 생성(Create)
@router.post("/", response_model=TripInDB, status_code=status.HTTP_201_CREATED)
async def create_trip(trip: TripCreate, db: AsyncSession = Depends(get_db)):
    return await trip_service.create_trip(db, trip)

# ✅ 특정 사용자의 가장 가까운 여행 (도시 정보 포함) //윤호식 추가
@router.get("/next/{user_id}")
async def get_next_trip_with_city(user_id: int, db: AsyncSession = Depends(get_db)):
    return await trip_service.get_next_trip_with_city(db, user_id)

# 여행 조회(Read)
@router.get("/{trip_id}", response_model=TripInDB)
async def get_trip(trip_id: int, db: AsyncSession = Depends(get_db)):
    return await trip_service.get_trip(db, trip_id)

# 특정 사용자의 모든 여행 조회(Read)
@router.get("/user/{user_id}", response_model=List[TripInDB])
async def get_trips_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await trip_service.get_trips_by_user(db, user_id)

# 여행 수정(Update)
@router.put("/{trip_id}", response_model=TripInDB)
async def update_trip(trip_id: int, trip_update: TripUpdate, db: AsyncSession = Depends(get_db)):
    return await trip_service.update_trip(db, trip_id, trip_update)

# 여행 삭제(Delete)
@router.delete("/{trip_id}", response_model=TripInDB)
async def delete_trip(trip_id: int, db: AsyncSession = Depends(get_db)):
    return await trip_service.delete_trip(db, trip_id)


# 2. 일자별 여행 계획(TripDay) 관련 API 엔드포인트

# 일자별 여행 계획 생성(Create)
@router.post("/days", response_model=TripDayInDB, status_code=status.HTTP_201_CREATED)
async def create_trip_day(trip_day: TripDayCreate, db: AsyncSession = Depends(get_db)):
    return await trip_service.create_trip_day(db, trip_day)

# 특정 여행의 모든 일자별 여행 계획 조회(Read)
@router.get("/days/{trip_id}", response_model=List[TripDayInDB])
async def get_trip_days_by_trip(trip_id: int, db: AsyncSession = Depends(get_db)):
    return await trip_service.get_trip_days_by_trip(db, trip_id)


# 3. 세부 일정(Schedule) 관련 API 엔드포인트

# 세부 일정 생성(Create)
@router.post("/schedules", response_model=ScheduleInDB, status_code=status.HTTP_201_CREATED)
async def create_schedule(schedule: ScheduleCreate, db: AsyncSession = Depends(get_db)):
    return await trip_service.create_schedule(db, schedule)

# 세부 일정 조회(Read)
@router.get("/schedules/{schedule_id}", response_model=ScheduleInDB)
async def get_schedule(schedule_id: int, db: AsyncSession = Depends(get_db)):
    return await trip_service.get_schedule(db, schedule_id)

# 특정 일자별 여행 계획의 모든 세부 일정 조회(Read)
@router.get("/schedules/day/{trip_day_id}", response_model=List[ScheduleInDB])
async def get_schedules_by_trip_day(trip_day_id: int, db: AsyncSession = Depends(get_db)):
    return await trip_service.get_schedules_by_trip_day(db, trip_day_id)

# 세부 일정 수정(Update)
@router.put("/schedules/{schedule_id}", response_model=ScheduleInDB)
async def update_schedule(schedule_id: int, schedule_update: ScheduleUpdate, db: AsyncSession = Depends(get_db)):
    return await trip_service.update_schedule(db, schedule_id, schedule_update)

# 세부 일정 삭제(Delete)
@router.delete("/schedules/{schedule_id}", response_model=ScheduleInDB)
async def delete_schedule(schedule_id: int, db: AsyncSession = Depends(get_db)):
    return await trip_service.delete_schedule(db, schedule_id)

# 4. 체크리스트 항목(ChecklistItem) 관련 API 엔드포인트

# 체크리스트 항목 생성(Create)
@router.post("/checklist-items", response_model=ChecklistItemInDB, status_code=status.HTTP_201_CREATED)
async def create_checklist_item(item: ChecklistItemCreate, db: AsyncSession = Depends(get_db)):
    return await trip_service.create_checklist_item(db, item)

# 체크리스트 항목 조회(Read)
@router.get("/checklist-items/{item_id}", response_model=ChecklistItemInDB)
async def get_checklist_item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await trip_service.get_checklist_item(db, item_id)

# 특정 여행의 모든 체크리스트 항목 조회(Read)
@router.get("/checklist-items/trip/{trip_id}", response_model=List[ChecklistItemInDB])
async def get_checklist_items_by_trip(trip_id: int, db: AsyncSession = Depends(get_db)):
    return await trip_service.get_checklist_items_by_trip(db, trip_id)

# 체크리스트 항목 수정(Update)
@router.put("/checklist-items/{item_id}", response_model=ChecklistItemInDB)
async def update_checklist_item(item_id: int, item_update: ChecklistItemUpdate, db: AsyncSession = Depends(get_db)):
    return await trip_service.update_checklist_item(db, item_id, item_update)

# 체크리스트 항목 삭제(Delete)
@router.delete("/checklist-items/{item_id}", response_model=ChecklistItemInDB)
async def delete_checklist_item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await trip_service.delete_checklist_item(db, item_id)