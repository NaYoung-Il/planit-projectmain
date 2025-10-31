from fastapi import APIRouter, UploadFile, File
from fastapi import  UploadFile, File, Depends
from fastapi.responses import StreamingResponse

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.photo import PhotoService
from app.db.schema.photo import PhotoRead
from app.services.review import get_current_user_id
import io


router = APIRouter(prefix='/reviews/{review_id}/photos',tags=['Photo'])

# 사진업로드
@router.post('/', response_model=PhotoRead)
async def upload_photo(review_id:int, 
                       user_id:int=Depends(get_current_user_id),
                       file:UploadFile = File(None),
                       db:AsyncSession=Depends(get_db)):
    return await PhotoService.create_image(db,review_id,user_id,file)

# 본문-해당 리뷰의 사진'리스트'
@router.get('/', response_model=list[PhotoRead])
async def get_photos(review_id:int,db:AsyncSession=Depends(get_db)):
    photo_list = await PhotoService.get_all_photo(db,review_id)
    print(photo_list)      
    return photo_list

# 대표사진 이미지 조회
@router.get('/{photo_id}', response_model=PhotoRead)
async def get_one_photo(review_id:int,photo_id:int,db:AsyncSession=Depends(get_db)):
    db_photo = await PhotoService.get_photo(db,review_id,photo_id)
    return db_photo

# 클릭시 이미지 원본 보여주기
@router.get('/{photo_id}/raw', response_model=PhotoRead)
async def get_photo_raw(review_id:int, photo_id:int, db:AsyncSession=Depends(get_db)):
    db_photo = await PhotoService.get_photo(db,review_id,photo_id)

    # 저장된 파일 확장자에 따라 mime-type 설정 (content_type)
    return StreamingResponse(io.BytesIO(db_photo.data),
                             media_type=db_photo.content_type
                             )
# 올린이미지 삭제
@router.delete('/{photo_id}', description='Delete Photo')
async def delete_photo(photo_id:int,                       
                       user_id:int=Depends(get_current_user_id),
                       db:AsyncSession=Depends(get_db)):
    db_photo = await PhotoService.delete_photo_by_id(db,photo_id,user_id)
    print(db_photo)
    return db_photo