from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.db.model.cities import City
from app.db.schema.cities import CityCreate

# 도시 생성(Create) - 관리자용
async def create_city(db: AsyncSession, city: CityCreate) -> City:
    db_city = City(**city.model_dump())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city

# 도시 조회(Read)
async def get_city(db: AsyncSession, city_id: int) -> Optional[City]:
    result = await db.execute(select(City).filter(City.id == city_id))
    return result.scalars().first()

# 도시 이름으로 조회(Read) - 사용자 선택용
async def get_city_by_name(db: AsyncSession, city_name: str) -> Optional[City]:
    result = await db.execute(select(City).filter(City.city_name == city_name))
    return result.scalars().first()

# 모든 도시 조회(Read) - 사용자 선택용
async def get_all_cities(db: AsyncSession) -> List[City]:
    result = await db.execute(select(City))
    return result.scalars().all()

# 도시 삭제(Delete) - 관리자용
async def delete_city(db: AsyncSession, city_id: int) -> Optional[City]:
    db_city = await get_city(db, city_id)
    if db_city:
        await db.delete(db_city)
        await db.commit()
    return db_city