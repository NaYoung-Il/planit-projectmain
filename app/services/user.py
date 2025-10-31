from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from datetime import datetime
from app.db.crud import user as user_crud
from app.db.schema.user import UserUpdate


#회원가입
async def register_user(db: AsyncSession, username: str, email: str, password: str):
    # 중복 이메일 체크
    existing_email = await user_crud.get_user_by_email(db, email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 중복 username 체크
    existing_username = await user_crud.get_user_by_username(db, username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    hashed_pw = hash_password(password)
    return await user_crud.create_user(db, username, email, hashed_pw)

#로근인
async def login_user(db: AsyncSession, email: str, password: str) -> str | None:
    user = await user_crud.get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return None

    return create_access_token(data={"sub": str(user.id)})


#유저 정보 조회(개인)
async def get_user(db: AsyncSession, email:str):
    user = await user_crud.get_user_by_email(db,email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Not Found"
        )
    
    return user


#모든 유저 정보 조회
async def read_all_user(db: AsyncSession):
    users = await user_crud.get_all_user(db)
    return users

#유저 삭제 
async def delete_user(db: AsyncSession, user_id: int):
    is_deleted = await user_crud.delete_user(db, user_id)
    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found."
        )
    return {"message": "User deleted successfully"}

#유저 업데이트
async def update_user(db: AsyncSession, user_id: int ,user_data:UserUpdate):
    hashed_password = None
    if user_data.password:
        hashed_password = hash_password(user_data.password)

    updated_user = await user_crud.update_user(
        db,
        user_id=user_id,
        user_name=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not Found"
        )

    return updated_user   