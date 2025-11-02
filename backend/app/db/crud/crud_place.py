from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.db.model.places import Place
from app.db.schema.places import PlaceCreate

# 장소 생성(Create)
async def create_place(db: AsyncSession, place: PlaceCreate) -> Place:
    db_place = Place(**place.model_dump())
    db.add(db_place)
    await db.commit()
    await db.refresh(db_place)
    return db_place

# 장소 조회(Read)
async def get_place(db: AsyncSession, place_id: int) -> Optional[Place]:
    result = await db.execute(select(Place).filter(Place.id == place_id))
    return result.scalars().first()

# 모든 장소 조회(Read)
async def get_all_places(db: AsyncSession) -> List[Place]:
    result = await db.execute(select(Place))
    return result.scalars().all()

# 특정 도시의 모든 장소 조회(Read)
async def get_places_by_city(db: AsyncSession, city_id: int) -> List[Place]:
    result = await db.execute(select(Place).filter(Place.city_id == city_id))
    return result.scalars().all()

# 장소 삭제(Delete)
async def delete_place(db: AsyncSession, place_id: int) -> Optional[Place]:
    db_place = await get_place(db, place_id)
    if db_place:
        await db.delete(db_place)
        await db.commit()
    return db_place