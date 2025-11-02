from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.db.model import City
from app.services.weather import WeatherService

from app.core.settings import settings


router = APIRouter(prefix="/weather", tags=["Weather"])

#도시이름으로 외부api 조회 및 DB저장
@router.get("/",description='Get and Create Weather')
async def get_weather_by_city_url(city:str,db:AsyncSession=Depends(get_db)):
    res = await WeatherService.get_weather(db,city)   #front axios 변수 res
    return  res

# 30일 지난 데이터 삭제 (관리자 의존성 추가 가능) Weather.created_at기준 30일
@router.delete("/delete-old-weather", description="30일지난 데이터 삭제")
async def cleanup_weather(db:AsyncSession=Depends(get_db)):
    result = await WeatherService.delete_old_weather(db)
    return result

#city_id 기반으로 조회 :  여행계획trip에서  # {city_id}가 위에있으면 error
@router.get("/{city_id}")
async def get_weather_by_city_id(city_id: int, db: AsyncSession = Depends(get_db)):
     
    city = await db.get(City, city_id)
    print(city)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    return await WeatherService.get_weather(db, city.city_name)