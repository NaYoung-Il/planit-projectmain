from pydantic import BaseModel
from typing import Optional

class PlaceBase(BaseModel):
    city_id: int
    place_name: Optional[str] = None
    type_id: int
    place_intro: Optional[str] = None
    is_popular: Optional[bool] = False

class PlaceCreate(PlaceBase):
    pass

class PlaceInDB(PlaceBase):
    id: int

    class Config:
        from_attributes = True