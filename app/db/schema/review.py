from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List
from app.db.schema.comment import CommentRead
from app.db.schema.photo import PhotoRead
##ReviewBase
class ReviewBase(BaseModel):
    title: str #= Field(..., max_length=255, min_length=1)
    content:str #= Field(...,min_length=1)
    rating:int = Field(..., ge=1, le=5)
    trip_id:int = Field(...,ge=1)

#Create
class ReviewCreate(ReviewBase):
    pass

#Update
class ReviewUpdate(BaseModel):
    title: str|None = None
    content:str|None = None
    rating: int|None = None
    trip_id: int|None = None

#Read
class ReviewInDB(ReviewBase):
    id: int = Field(..., alias="review_id")
    user_id:int
    created_at:datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    #orm->pydantic
    class Config:
        from_attributes = True
        populate_by_name =True # id - review_id alias 호환성
#safeuser
class SafeUser(BaseModel):
     user_id:int
     username:str |None
    
class ReviewRead(ReviewInDB):        
        username: str | None = None #JOIN 후 None삭제
        like_count: int = 0 #출력 전용 필드, DB/ORM없음 ,count()로 계산 ->조회전용
        # trip_id: int
        city_id: int
        city_name: str
        comments: list[CommentRead] = []
        photo_url: str | None
        # file: PhotoRead | None = Field(default=None, alias="photo")

class oneReviewRead(ReviewInDB):
     trip_id: int
     photo_url: str | None

##Like
class LikeCreate(BaseModel):
     review_id: int

#Like응답 (user_id는 JWT에서 추출)
class LikeResponse(BaseModel):
     review_id: int
     like_count: int  #출력 전용 필드, DB/ORM없음 ,count()로 계산->좋아요토글
     liked: bool               #버튼 클릭시 최신값 업데이트

  