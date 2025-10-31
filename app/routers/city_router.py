from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.services.city_service import CityService
from app.db.schema.cities import CityCreate, CityInDB
from app.db.schema.places import PlaceCreate, PlaceInDB
from sqlalchemy import select, func
city_service = CityService()
router = APIRouter(prefix="/cities", tags=["Cities & Places"])

# 2. 장소(Place) 관련 API 엔드포인트 -> 경로 충돌 문제 때문에 순서 변경

# 장소 생성(Create)
@router.post("/places", response_model=PlaceInDB, status_code=status.HTTP_201_CREATED)
async def create_place(place: PlaceCreate, db: AsyncSession = Depends(get_db)):
    return await city_service.create_place(db, place)

# 장소 조회(Read)
@router.get("/places/{place_id}", response_model=PlaceInDB)
async def get_place(place_id: int, db: AsyncSession = Depends(get_db)):
    return await city_service.get_place(db, place_id)

# 모든 장소 조회(Read)
@router.get("/places", response_model=List[PlaceInDB])
async def get_all_places(db: AsyncSession = Depends(get_db)):
    return await city_service.get_all_places(db)

# 특정 도시의 모든 장소 조회(Read)
@router.get("/places/city/{city_id}", response_model=List[PlaceInDB])
async def get_places_by_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await city_service.get_places_by_city(db, city_id)

# 장소 삭제(Delete)
@router.delete("/places/{place_id}", response_model=PlaceInDB)
async def delete_place(place_id: int, db: AsyncSession = Depends(get_db)):
    return await city_service.delete_place(db, place_id)


# 1. 도시(City) 관련 API 엔드포인트

# 도시 생성(Create) #수정 or 삭제필요###
@router.post("/", response_model=CityInDB, status_code=status.HTTP_201_CREATED)
async def create_city(city: CityCreate, db: AsyncSession = Depends(get_db)):
    return await city_service.create_city(db, city)

# 도시 조회(Read)
@router.get("/{city_id}", response_model=CityInDB)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await city_service.get_city(db, city_id)

# 모든 도시 조회(Read)
@router.get("/", response_model=List[CityInDB])
async def get_all_cities(db: AsyncSession = Depends(get_db)):
    return await city_service.get_all_cities(db)

# 도시 이름으로 조회(Read)
@router.get("/name/{city_name}", response_model=CityInDB)
async def get_city_by_name(city_name: str, db: AsyncSession = Depends(get_db)):
    return await city_service.get_city_by_name(db, city_name)

# 도시 삭제(Delete)
@router.delete("/{city_id}", response_model=CityInDB)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await city_service.delete_city(db, city_id)

import pandas as pd
from app.db.model.cities import City
#도시 일괄추가(from xlsx)
@router.post('/init')
async def init(db:AsyncSession=Depends(get_db)):
        count = await db.scalar(select(func.count()).select_from(City))
        if count == 0:
            df = pd.read_excel("cities_list_ko.xlsx")
            for _, row in df.iterrows():
                db.add(City(
                    city_name=row["name"],
                    lat=row["lat"],
                    lon=row["lon"],
                    country=row["country"],
                    ko_name=row["ko_name"],
                    ko_country=row["ko_country"]
                ))
            await db.commit()
        return {'msg':'도시 목록 추가완료'}