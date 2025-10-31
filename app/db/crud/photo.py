from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Photo, Review
from sqlalchemy import select, or_, desc, func
from typing import Optional


#사진은 로컬폴더나, 외부환경(외부스토리지)에 저장


class PhotoCrud:
    #photo_id조회 - 대표사진 하나 조회용 (review_id가 필요한가?)
    @staticmethod
    async def get_photo_id(db:AsyncSession,photo_id:int):
        return await db.get(Photo, photo_id)

    @staticmethod
    async def create(db:AsyncSession,                      
                     review_id:int, 
                     filename:str,
                     data:bytes,
                     content_type:str):    
        db_photo = Photo(review_id=review_id,filename=filename,data=data,content_type=content_type)
        db.add(db_photo)
        await db.flush()
        return db_photo
    
    @staticmethod
    async def get_all(db:AsyncSession, review_id:int):
        query = select(Photo).where(Photo.review_id==review_id)
        result = await db.execute(query)
        photos= result.scalars().all()
        # print('crud return:', photos, type(photos))
        return photos
    

    @staticmethod
    async def delete_by_id(db:AsyncSession, photo_id:int, user_id:int)->bool:
        photo = await db.get(Photo, photo_id)
        if not photo :        
            return False
        #photo_id를 입력한 photo객체의 삭제할 review_id를 Review테이블에서져와야함
        review = await db.get(Review, photo.review_id) 
        #검증기능 완료후 추가
        # if not review or review.user_id != user_id:
        #     return False
        if not review:
            return False
        await db.delete(photo) #선택한 photo_id의 row삭제
        await db.flush()
        return True 
    
    