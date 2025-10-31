from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# 그룹 관련 스키마

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None

class GroupCreate(GroupBase):
    pass

class GroupResponse(GroupBase):
    id: int

    class Config:
        orm_mode = True