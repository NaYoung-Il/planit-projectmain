from pydantic import BaseModel

class CityInDB(BaseModel): # 추가 : City 응답용
    id: int
    ko_name: str
    ko_country: str
    city_name: str
    
    class Config:
        from_attributes = True