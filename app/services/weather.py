from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Weather, City, CityWeather
from app.db.schema.weather import WeatherBase
from app.db.crud import WeatherCrud
from app.services import CityService
from app.routers.user import Auth_Dependency
from sqlalchemy import select
from typing import Optional
from sqlalchemy import select, or_, desc, func, delete
from app.core.settings import settings
from datetime import datetime, timedelta
import httpx
import json
class WeatherService:
    #외부 api 호출 후 DB저장 기초호출만구현//
    #  DB저장후 3시간 이내 재요청시 저장된값 DB에서 호출추가(외부호출누수 방지) 
    #1도시조회
    #2db캐시확인 조건분기(3h이상 3h 미만)
    #3 city_name / get city_id join / 외부 api호출
    @staticmethod
    async def get_weather(db:AsyncSession,city:str):
        #도시 조회
        result = await db.execute(select(City).where(City.city_name==city))
        db_city = result.scalars().first() #도시정보

        if not db_city:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='도시없음')
        lat = db_city.lat
        lon = db_city.lon

        # -----------------------------------------------------------------
        # [수정] 캐시 조회 로직 (M2M Join 사용)
        # -----------------------------------------------------------------
        three_hours_ago = datetime.utcnow() - timedelta(hours=3)
        
        # 2. City -> CityWeather -> Weather 순으로 조인하여 최신 날씨 탐색
        stmt = select(Weather).join(
            CityWeather, Weather.id == CityWeather.weather_id
        ).where(
            CityWeather.city_id == db_city.id,  # 이 도시(city_id)의 날씨 중
            Weather.date >= three_hours_ago     # 3시간 이내의 날씨
        ).order_by(desc(Weather.date)).limit(1) # 가장 최신 것
        
        cached_result = await db.execute(stmt)
        db_weather = cached_result.scalars().first() # 가장 최신의 유효한 캐시

        # 3. 캐시 유효성 검사
        if db_weather:
            # 캐시가 있으면 DB 데이터를 파싱하여 반환
            print("db에서나간날씨id:",db_weather.id)
            return json.loads(db_weather.weather_info)
        
        # 4. 캐시가 없으면 외부 API 호출
        print(f"Fetching new weather from API for {city}") # 디버깅용
        url = "https://api.openweathermap.org/data/3.0/onecall"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": settings.openweather_api_key,
            "units": 'metric',
            "lang": 'kr'
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)

            if response.status_code != 200:
                # API 호출 실패 시
                raise HTTPException(status_code=response.status_code, detail=response.json())
                
            data=response.json()

        # Weather 테이블에 새 데이터 저장
        new_weather = await WeatherCrud.create(db=db, weather_data=data)
            
        # city_weather 중간테이블 저장
        db.add(CityWeather(city_id=db_city.id, weather_id=new_weather.id))

        await db.commit()        

        return data
        
    #delete
    @staticmethod
    async def delete_old_weather(db:AsyncSession):
        expired_date = datetime.utcnow() - timedelta(days=30)
        await db.execute(delete(Weather).where(Weather.date < expired_date))
        await db.commit()
        return {"msg":"30일 지난 데이터 삭제 완료"}
        
            
