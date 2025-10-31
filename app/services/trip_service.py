from fastapi import HTTPException, status
#윤호식 추가
from sqlalchemy import text 
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.db.crud import crud_trip, crud_city
from app.db.model.trip import Trip
from app.db.model.trip_day import TripDay
from app.db.model.schedule import Schedule
from app.db.model.checklist_item import ChecklistItem
from app.db.schema.trip import TripCreate, TripUpdate
from app.db.schema.trip_day import TripDayCreate
from app.db.schema.schedule import ScheduleCreate, ScheduleUpdate
from app.db.schema.checklist_item import ChecklistItemCreate, ChecklistItemUpdate

class TripService:

    ## 1. 여행(Trip) 관련 서비스 메서드
    
    # 여행 생성(Create) - 도시 ID가 유효한지 확인
    async def create_trip(self, db: AsyncSession, trip: TripCreate) -> Trip:
        city = await crud_city.get_city(db, trip.city_id)
        if not city:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="도시를 찾을 수 없습니다.")
        new_trip = await crud_trip.create_trip(db, trip)
        return new_trip
    
    # 여행 조회(Read)
    async def get_trip(self, db: AsyncSession, trip_id: int) -> Optional[Trip]:
        trip = await crud_trip.get_trip(db, trip_id)
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="여행을 찾을 수 없습니다.")
        return trip
    
    # 특정 사용자의 모든 여행 조회(Read)
    async def get_trips_by_user(self, db: AsyncSession, user_id: int) -> List[Trip]:
        trips = await crud_trip.get_trips_by_user(db, user_id)
        return trips
    
    # 여행 수정(Update) - 도시 ID가 유효한지 확인
    async def update_trip(self, db: AsyncSession, trip_id: int, trip_update: TripUpdate) -> Optional[Trip]:
        if trip_update.city_id:
            city = await crud_city.get_city(db, trip_update.city_id)
            if not city:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="도시를 찾을 수 없습니다.")
        updated_trip = await crud_trip.update_trip(db, trip_id, trip_update)
        if not updated_trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="여행을 찾을 수 없습니다.")
        return updated_trip
    
    # 여행 삭제(Delete)
    async def delete_trip(self, db: AsyncSession, trip_id: int) -> Optional[Trip]:
        deleted_trip = await crud_trip.delete_trip(db, trip_id)
        if not deleted_trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="여행을 찾을 수 없습니다.")
        return deleted_trip
    
    ## 2. 일자별 여행 계획(TripDay) 관련 서비스 메서드
    
    # 일자별 여행 계획 생성(Create)
    async def create_trip_day(self, db: AsyncSession, trip_day: TripDayCreate) -> TripDay:
        trip = await crud_trip.get_trip(db, trip_day.trip_id)
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="일자별 여행 계획을 찾을 수 없습니다.")
        new_trip_day = await crud_trip.create_trip_day(db, trip_day)
        return new_trip_day
    
    # 특정 여행의 모든 일자별 여행 계획 조회(Read)
    async def get_trip_days_by_trip(self, db: AsyncSession, trip_id: int) -> List[TripDay]:
        trip_days = await crud_trip.get_trip_days_by_trip(db, trip_id)
        return trip_days
    
    ## 3. 세부 일정(Schedule) 관련 서비스 메서드

    # 세부 일정 생성(Create)
    async def create_schedule(self, db: AsyncSession, schedule: ScheduleCreate) -> Schedule:
        trip_day = await crud_trip.get_trip_day(db, schedule.trip_day_id)
        if not trip_day:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="세부 일정을 찾을 수 없습니다.")
        new_schedule = await crud_trip.create_schedule(db, schedule)
        return new_schedule
    
    # 세부 일정 조회(Read)
    async def get_schedule(self, db: AsyncSession, schedule_id: int) -> Optional[Schedule]:
        schedule = await crud_trip.get_schedule(db, schedule_id)
        if not schedule:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="세부 일정을 찾을 수 없습니다.")
        return schedule
    
    # 특정 일자별 여행 계획의 모든 세부 일정 조회(Read)
    async def get_schedules_by_trip_day(self, db: AsyncSession, trip_day_id: int) -> List[Schedule]:
        schedules = await crud_trip.get_schedules_by_trip_day(db, trip_day_id)
        return schedules
    
    # 세부 일정 수정(Update)
    async def update_schedule(self, db: AsyncSession, schedule_id: int, schedule_update: ScheduleUpdate) -> Optional[Schedule]:
        updated_schedule = await crud_trip.update_schedule(db, schedule_id, schedule_update)
        if not updated_schedule:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="세부 일정을 찾을 수 없습니다.")
        return updated_schedule
    
    # 세부 일정 삭제(Delete)
    async def delete_schedule(self, db: AsyncSession, schedule_id: int) -> Optional[Schedule]:
        deleted_schedule = await crud_trip.delete_schedule(db, schedule_id)
        if not deleted_schedule:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="세부 일정을 찾을 수 없습니다.")
        return deleted_schedule
    
    ## 4. 체크리스트 항목(ChecklistItem) 관련 서비스 메서드

    # 체크리스트 항목 생성(Create)
    async def create_checklist_item(self, db: AsyncSession, checklist_item: ChecklistItemCreate) -> ChecklistItem:
        new_item = await crud_trip.create_checklist_item(db, checklist_item)
        return new_item
    
    # 체크리스트 항목 수정(Update)
    async def update_checklist_item(self, db: AsyncSession, item_id: int, item_update: ChecklistItemUpdate) -> Optional[ChecklistItem]:
        updated_item = await crud_trip.update_checklist_item(db, item_id, item_update)
        if not updated_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="체크리스트 항목을 찾을 수 없습니다.")
        return updated_item
    
    # 체크리스트 항목 삭제(Delete)
    async def delete_checklist_item(self, db: AsyncSession, item_id: int)   -> Optional[ChecklistItem]:
        deleted_item = await crud_trip.delete_checklist_item(db, item_id)
        if not deleted_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="체크리스트 항목을 찾을 수 없습니다.")
        return deleted_item
    
    # 체크리스트 항목 조회(Read)
    async def get_checklist_item(self, db: AsyncSession, item_id: int) -> Optional[ChecklistItem]:
        item = await crud_trip.get_checklist_item(db, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="체크리스트 항목을 찾을 수 없습니다.")
        return item
    
    # 특정 여행의 모든 체크리스트 항목 조회(Read)
    async def get_checklist_items_by_trip(self, db: AsyncSession, trip_id: int) -> List[ChecklistItem]:
        items = await crud_trip.get_checklist_items_by_trip(db, trip_id)
        return items
    
    # ✅ 특정 사용자의 가장 가까운 여행 + 도시 정보 포함 (알림용) //윤호식 추가
    async def get_next_trip_with_city(self, db: AsyncSession, user_id: int):
        query = text("""
            SELECT t.id, t.title, t.start_date, t.end_date,
                   c.city_name, c.lat, c.lon
            FROM trip t
            JOIN cities c ON t.city_id = c.id
            WHERE t.user_id = :user_id
            ORDER BY t.start_date ASC
            LIMIT 1
        """)
        result = await db.execute(query, {"user_id": user_id})
        row = result.first()
        if not row:
            return None

        return {
            "id": row.id,
            "title": row.title,
            "start_date": row.start_date,
            "end_date": row.end_date,
            "city_name": row.city_name,
            "lat": row.lat,
            "lon": row.lon,
        }