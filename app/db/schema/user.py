from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.db.schema.group import GroupResponse


# ----------------------
# 사용자 관련 스키마
# ----------------------
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    # 🔑 그룹 정보 포함
    groups: List[GroupResponse] = []

    class Config:
        orm_mode = True
        
