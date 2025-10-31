from fastapi import HTTPException,status, UploadFile, File
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Photo, Review
from app.db.crud import PhotoCrud
from sqlalchemy import select


class PhotoService:
    #사진생성 Create
    @staticmethod
    async def create_image(db:AsyncSession,review_id:int,user_id:int,file:UploadFile):
        result = await db.execute(select(Review).where(Review.id == review_id))
        db_review = result.scalars().first()
        if not db_review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='리뷰가 존재하지 않습니다')
        if db_review.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='본인이 작성한 리뷰에만 업로드가능')
        contents = await file.read()  #업로드된 파일을 읽어옴
        db_photo = await PhotoCrud.create(db=db,
                                          review_id=review_id,                                                                              
                                          filename=file.filename,
                                          content_type=file.content_type,
                                          data=contents)
        
        await db.flush()
        await db.refresh(db_photo)        
        return db_photo
    
    #사진 리스트 조회 Read
    @staticmethod
    async def get_all_photo(db:AsyncSession,review_id:int):
        result = await db.execute(select(Review).where(Review.id == review_id))
        db_review = result.scalars().first()
        if not db_review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='리뷰가 존재하지 않습니다')
        db_photo = await PhotoCrud.get_all(db,review_id)
        if not db_photo: 
            return [] #등록사진 없으면 빈배열
        print(db_photo)
        return db_photo      
        
    #사진 단일 조회(대표이미지/원본조회) 
    @staticmethod
    async def get_photo(db:AsyncSession,review_id:int,photo_id:int):  
        #리뷰 존재여부
        result = await db.execute(select(Review).where(Review.id == review_id))
        db_review = result.scalars().first()
        if not db_review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='리뷰가 존재하지 않습니다')
        #사진 검증        
        query = select(Photo).where(Photo.id == photo_id,
                                    Photo.review_id == review_id)        
        result = await db.execute(query)
        db_photo = result.scalar_one_or_none()
        if not db_photo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='사진이 존재하지 않습니다')
        return db_photo
    
    #사진 삭제 Delete
    @staticmethod
    async def delete_photo_by_id(db:AsyncSession,photo_id:int,user_id:int)->bool:
        db_photo = await PhotoCrud.get_photo_id(db,photo_id)
        if not db_photo:
            raise HTTPException(status_code=404, detail='사진없음')
        
        deleted_photo = await PhotoCrud.delete_by_id(db,photo_id,user_id)
        if deleted_photo:
            await db.flush()
            return deleted_photo
        
