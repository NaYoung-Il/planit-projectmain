from pydantic import BaseModel, Field
from datetime import datetime, timezone

#comment // front-> update, delete 기능 필요
class CommentBase(BaseModel):
    content:str = Field(..., min_length=1)

#create (reviews/{review_id}/comments)
class CommentCreate(CommentBase):
    pass

#Update
class CommentUpdate(BaseModel):
    content:str | None = None  #호환성 Optional[str]


#Output model
class CommentInDB(CommentBase):
    id: int
    user_id:int
    review_id:int    
    created_at: datetime

    class Config:
        from_attributes=True

#Read(Response전용)
class CommentRead(CommentInDB):    
    username: str |None = None #JOIN결과
    