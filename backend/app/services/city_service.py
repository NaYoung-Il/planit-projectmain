from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.crud import crud_city, crud_place
from app.db.model.cities import City
from app.db.model.places import Place
from app.db.schema.cities import CityCreate
from app.db.schema.places import PlaceCreate

class CityService:

    ## 1. 도시(City) 관련 서비스 메서드
    
    # 도시 생성(Create) - 관리자용
    async def create_city(self, db: AsyncSession, city: CityCreate) -> City:
        new_city = await crud_city.create_city(db, city)
        return new_city
    
    # 도시 조회(Read)
    async def get_city(self, db: AsyncSession, city_id: int) -> Optional[City]:
        city = await crud_city.get_city(db, city_id)
        if not city:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="도시를 찾을 수 없습니다.")
        return city
    
    # 도시 이름으로 조회(Read) - 사용자 선택용
    async def get_city_by_name(self, db: AsyncSession, city_name: str) -> Optional[City]:
        city = await crud_city.get_city_by_name(db, city_name)
        if not city:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="도시를 찾을 수 없습니다.")
        return city
    
    # 모든 도시 조회(Read) - 사용자 선택용
    async def get_all_cities(self, db: AsyncSession) -> List[City]:
        cities = await crud_city.get_all_cities(db)
        return cities
    
    # 도시 삭제(Delete) - 관리자용
    async def delete_city(self, db: AsyncSession, city_id: int) -> Optional[City]:
        deleted_city = await crud_city.delete_city(db, city_id)
        if not deleted_city:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="도시를 찾을 수 없습니다.")
        return deleted_city
    
    ## 2. 장소(Place) 관련 서비스 메서드
    
    # 장소 생성(Create)
    async def create_place(self, db: AsyncSession, place: PlaceCreate) -> Place:
        # 장소 생성 시 해당 도시가 존재하는지 확인
        city = await crud_city.get_city(db, place.city_id)
        if not city:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="도시를 찾을 수 없습니다.")
        new_place = await crud_place.create_place(db, place)
        return new_place
    
    # 장소 조회(Read)
    async def get_place(self, db: AsyncSession, place_id: int) -> Optional[Place]:
        place = await crud_place.get_place(db, place_id)
        if not place:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="장소를 찾을 수 없습니다.")
        return place
    
    # 모든 장소 조회(Read)
    async def get_all_places(self, db: AsyncSession) -> List[Place]:
        places = await crud_place.get_all_places(db)
        return places
    
    # 특정 도시의 모든 장소 조회(Read)
    async def get_places_by_city(self, db: AsyncSession, city_id: int) -> List[Place]:
        # 도시가 존재하는지 확인
        city = await crud_city.get_city(db, city_id)
        if not city:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="도시를 찾을 수 없습니다.")
        places = await crud_place.get_places_by_city(db, city_id)
        return places
    
    # 장소 삭제(Delete)
    async def delete_place(self, db: AsyncSession, place_id: int) -> Optional[Place]:
        deleted_place = await crud_place.delete_place(db, place_id)
        if not deleted_place:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="장소를 찾을 수 없습니다.")
        return deleted_place