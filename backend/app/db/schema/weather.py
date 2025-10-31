from pydantic import BaseModel, Field
from datetime import datetime, timedelta, timezone
from typing import Optional


class WeatherBase(BaseModel):
    weather_info: dict
    date : datetime

class WeatherCreate(WeatherBase):
    pass

class CityWeather(BaseModel):
    city_id: int
    weather_id: int
