from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Weather
from app.db.schema.weather import WeatherCreate
from sqlalchemy import select, or_, desc, func,and_
from typing import Optional
from datetime import datetime, timedelta
import json
class WeatherCrud:
    @staticmethod
    async def create(db: AsyncSession,
                        weather_data: dict,
                    ):
        # 수정 : Weather 모델에는 weather_info와 date만 존재하므로
        # city_name, lat, lon 필드는 제거
        weather_info=json.dumps(weather_data)
        new_weather = Weather(
            weather_info = weather_info,
            date = datetime.utcnow(),
        )
        db.add(new_weather)
        await db.flush()
        return new_weather
    
    @staticmethod
    async def delete_old_weather(db:AsyncSession):
        pass