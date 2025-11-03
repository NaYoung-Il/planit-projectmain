from fastapi import HTTPException, status
#윤호식 추가
from sqlalchemy import text, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import timedelta
from app.db.crud import crud_trip, crud_city
from app.db.model.trip import Trip
from app.db.model.trip_day import TripDay
from app.db.model.trip_city import TripCity
from app.db.model.schedule import Schedule
from app.db.model.checklist_item import ChecklistItem
from app.db.schema.trip import TripCreate, TripUpdate
from app.db.schema.trip_day import TripDayCreate
from app.db.schema.trip_city import TripCityCreate, TripCityUpdate
from app.db.schema.schedule import ScheduleCreate, ScheduleUpdate
from app.db.schema.checklist_item import ChecklistItemCreate, ChecklistItemUpdate
from datetime import date

class TripService:

    ## 1. 여행(Trip) 관련 서비스 메서드
    
    # 여행 생성(Create) - 도시 ID가 유효한지 확인
    # 11/2 수정(나영일) : update_trip과 동일한 로직 처리
    async def create_trip(self, db: AsyncSession, trip: TripCreate) -> Trip:
        # 기존 city_id 유효성 검사 삭제
        # (새로운 M:N 관계에서는 FK 제약조건이 처리)
        
        # 1. Trip 기본 객체 생성
        new_trip = Trip(
            title=trip.title,
            start_date=trip.start_date,
            end_date=trip.end_date,
            user_id=trip.user_id,
        )

        # 2. TripCity 목록 생성 (update_trip 로직 동일)
        # (cascade에 의해 new_trip에 자동 연결됨)
        new_trip.trip_cities = [
            TripCity(
                city_id=city.city_id,
                start_date=city.start_date,
                end_date=city.end_date
            ) for city in trip.trip_cities
        ]

        # 4. TripDay 목록 생성 (update_trip 로직 동일)
        # (day_sequence 기반으로 생성)
        duration_days = (new_trip.end_date - new_trip.start_date).days + 1
        
        new_trip.trip_day = [
            TripDay(day_sequence=i)
            for i in range(1, duration_days + 1)
        ]

        # 5. 모든 객체(Trip, TripCity, TripDay)를 DB에 추가
        try:
            db.add(new_trip)
            await db.flush()    # 커밋 전에 flush하여 ID를 먼저 가져옴
            new_trip_id = new_trip.id   # 만료되지 않은 객체에서 ID를 안전하게 저장
            await db.commit()   # 트랜잭션 최종 커밋
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"DB Error on create: {e}")
        
        created_trip = await crud_trip.get_trip_with_relations(db, new_trip_id)
        if not created_trip:
            raise Exception("Failed to retrieve created trip")
            
        return created_trip
    
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
    
    # 11/2 추가(나영일)
    async def get_trip_cities_by_trip_id(self, db: AsyncSession, trip_id: int) -> List[TripCity]:
        trip_cities = await crud_trip.get_trip_cities(db, trip_id)
        return trip_cities

    # 여행 수정(Update) 
    # 11/2 수정(나영일) : 서비스에서 모든 로직 처리
    async def update_trip(self, db: AsyncSession, trip_id: int, trip_update: TripUpdate) -> Optional[Trip]:
        
        # 1. 원본 Trip을 'trip_day'와 'trip_cities' 모두와 함께 로드
        db_trip = await crud_trip.get_trip_with_relations(db, trip_id)

        if not db_trip:
            raise HTTPException(status_code=404, detail="Trip not found")

        # 2. 날짜 변경 감지를 위해 이전 기간을 계산
        old_duration_days = (db_trip.end_date - db_trip.start_date).days + 1
        
        # 3. Trip의 기본 정보(제목, 시작/종료일) 업데이트
        # 시작일이 바뀌어도 'trip_days'는 건드리지 않습니다.
        db_trip.title = trip_update.title
        db_trip.start_date = trip_update.start_date
        db_trip.end_date = trip_update.end_date
        
        # 4. TripCity 목록 교체 (cascade가 처리)
        db_trip.trip_cities = [
            TripCity(
                city_id=city.city_id,
                start_date=city.start_date,
                end_date=city.end_date
            ) for city in trip_update.trip_cities
        ]

        # 5. 새로운 기간 계산
        new_duration_days = (db_trip.end_date - db_trip.start_date).days + 1

        # 6. 기간 변경 로직 수행
        if new_duration_days < old_duration_days:
            # Case 1: 기간 축소
            # 새 기간보다 큰 'day_sequence'를 가진 TripDay를 목록에서 제거
            # cascade="all, delete-orphan"이 DB에서 이들을 삭제함
            db_trip.trip_day = [
                day for day in db_trip.trip_day 
                if day.day_sequence <= new_duration_days
            ]
            
        elif new_duration_days > old_duration_days:
            # Case 2: 기간 연장
            # 기존 기간 이후부터 새 기간까지 빈 TripDay 객체를 추가
            for i in range(old_duration_days + 1, new_duration_days + 1):
                db_trip.trip_day.append(
                    TripDay(day_sequence=i)
                )
        
        # 7. 모든 변경사항을 한 번에 커밋
        try:
            db.add(db_trip)
            await db.commit()
            await db.refresh(db_trip)
            await db.refresh(db_trip, attribute_names=['trip_cities', 'trip_day'])
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"DB Error: {e}")
        
        return db_trip
    
    # 여행 삭제(Delete)
    async def delete_trip(self, db: AsyncSession, trip_id: int) -> Optional[Trip]:
        db_trip = await db.get(Trip, trip_id)
        if not db_trip:
            raise HTTPException(status_code=404, detail="Trip not found")
        await db.delete(db_trip)
        await db.commit()
        return
    
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
    
    # 특정 사용자의 가장 가까운 여행 + 도시 정보 포함 (알림용) //윤호식 추가
    # 11/2 수정(나영일) : DB 구조 변경에 맞게 쿼리 수정
    async def get_next_trip_with_city(self, db: AsyncSession, user_id: int):
        """
        [수정]
        오늘 이후에 시작하는 가장 가까운 여행 1개를 찾아,
        M:N 관계(trip_cities)에서 첫 번째 도시 정보를 조합하여 반환합니다.
        """
        
        # 1. 오늘 날짜 이후로 가장 가까운 'Trip'을 먼저 찾습니다.
        today = date.today()
        stmt = select(Trip).where(
            Trip.user_id == user_id,
            Trip.start_date >= today
        ).order_by(Trip.start_date.asc()).limit(1) # ASC (오름차순)
        
        result = await db.execute(stmt)
        next_trip = result.scalars().first()

        if not next_trip:
            # 다가오는 여행이 없음
            return None

        # 2. 찾은 'Trip'의 ID를 사용해, Eager Loading이 적용된 전체 정보를 다시 불러옵니다.
        trip_with_relations = await crud_trip.get_trip_with_relations(db, next_trip.id)

        if not trip_with_relations:
            return None # (오류 방지)

        # 3. M:N 관계에서 첫 번째 도시 정보를 찾습니다.
        first_city = None
        if trip_with_relations.trip_cities:
            # 도시별 일정을 시작일 순서로 정렬 (선택 사항)
            trip_with_relations.trip_cities.sort(key=lambda x: x.start_date)
            # 0번째 도시의 'city' 객체를 가져옵니다.
            first_city = trip_with_relations.trip_cities[0].city

        # 4. 프론트엔드가 기대하는 형식(기존 SQL 쿼리 참고)으로 데이터를 조합하여 반환합니다.
        return {
            "id": trip_with_relations.id,
            "title": trip_with_relations.title,
            "start_date": trip_with_relations.start_date,
            "end_date": trip_with_relations.end_date,
            
            # ⬇'city_id'가 아닌 'trip_cities'에서 가져온 정보
            "city_name": first_city.ko_name if first_city else "도시 미정",
            "lat": first_city.lat if first_city else None,
            "lon": first_city.lon if first_city else None
        }