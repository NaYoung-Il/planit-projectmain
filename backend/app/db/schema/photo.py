from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional
class PhotoBase(BaseModel):
    filename:str
    

#Create
class PhotoCreate(PhotoBase):
    review_id: int

#Update - 사진은 파일교체 Delete+ create로 처리

#Read
class PhotoInDB(PhotoBase):
    photo_id:int = Field(None,alias="id")
    review_id:int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True 
        populate_by_name =True
class PhotoRead(PhotoInDB):
    pass
    