from fastapi import HTTPException,status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Review,Like,Trip,City, Photo
from app.db.schema.review import ReviewCreate, ReviewUpdate, LikeResponse, ReviewRead
from app.db.crud import ReviewCrud, LikeCrud
from app.routers.user import Auth_Dependency
from sqlalchemy import select
from typing import Optional
from sqlalchemy import select, or_, desc, func
from app.services.photo import PhotoService
from app.services.comment import CommentService
from app.core.settings import settings
# by_relationship- responsebody에 유저이름, 좋아요 수 추가헬퍼함수  
# #username  
def add_username(review:Review):    
    if review.users:
        review.username = review.users.username
    else:
        raise HTTPException(status_code=404,detail='작성자 정보 없음')
    return review
#like_count 
async def add_likecounts(db:AsyncSession,review:Review):           
    review.like_count=await LikeCrud.count_by_review(db,review.id)
    return review
#get currnet id -> 가능하면 user쪽으로 이전 (trip, city 생성시에도 쓸 수 있게)
async def get_current_user_id(currnet_user:Auth_Dependency):
    user_id = currnet_user.id
    return user_id
#city_name
def add_city_name(review:Review):
    if review.trip and review.trip.city:
        review.city_id = review.trip.city.id
        review.city_name = review.trip.city.city_name
    else: 
        raise HTTPException(status_code=404, detail='도시정보없음')
    return review

#리뷰
class ReviewService:
    #Create
    @staticmethod
    async def create(db:AsyncSession,
                     review_data:ReviewCreate, 
                     user_id:int,
                     trip_id:int,                     
                     ):
        #trip_id 유효성 검증
        trip = await db.get(Trip, trip_id)  #PK조회 전용
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='존재하지않는 여행계획입니다')
        
        db_review = await ReviewCrud.create(db, review_data,user_id,trip_id)
        # await db.commit() -get_db에서 commit 관리중 -> 삭제     
        await db.refresh(db_review)
        
        #orm 반환용 / user주입 / like_count 초기값 / city_id,cityname
        user_review = add_username(db_review)
        city_review = add_city_name(user_review)
        city_review.like_counts = 0
        # print("db_review",db_review)
        # print("city_review",city_review)              
       
        return db_review        
    
    #Read    
    #trip id에 해당하는 list조회(R) - 여행별 리뷰 / trip_id없을시 빈배열반환 []
    @staticmethod
    async def get_all_review(db:AsyncSession,
                      trip_id:Optional[int],
                      search:Optional[str]=None,
                      limit:int=100,
                      offset:int = 0):
        db_review = await ReviewCrud.get_all(db,search,limit,offset)
        #orm 반환용 / user주입 / like_count 초기값
        
        if not db_review:
            return []
        for review in db_review:
            add_username(review)
            add_city_name(review)
            await add_likecounts(db,review)  
            review_id=review.id
            # print("reviewid:",review_id)

            #comments []            
            comments=await CommentService.get_all_comment(db,review_id, None, 10, 0)
            if comments:
                for comment in comments:
                    add_username(comment)
            review.comments = comments or []

            #photo_url
            photo_result =await db.execute(select(Photo.id).where(Photo.review_id==review.id))
            db_photo_id = photo_result.scalar()
            # print("db_photos\.id:",db_photo_id)
            if db_photo_id:         
                    # review.photo_url=f'{settings.backend_url}/reviews/{review_id}/photos/{db_photo_id}/raw'
                    review.photo_url=f'http://localhost:8081/reviews/{review_id}/photos/{db_photo_id}/raw'
                    # print("photo_url:",review.photo_url)
            else:
                review.photo_url=None                

        return db_review

    #review_id로 개별조회
    @staticmethod
    async def get_review(db:AsyncSession,review_id:int):
        db_review = await ReviewCrud.get_id(db,review_id)  
        if not db_review:
            raise HTTPException(status_code=404, detail="리뷰가 없습니다")     
        if not db_review.users:
            raise HTTPException(status_code=404, detail='작성자 정보 없음')
        
        print()
        #username
        add_username(db_review)
        #city_name
        add_city_name(db_review)
        #like_count       
        await add_likecounts(db,db_review)
        #photo_url 추가
        photo_result =await db.execute(select(Photo.id).where(Photo.review_id==db_review.id))
        db_photo_id = photo_result.scalar()
        # print("db_photos\.id:",db_photo_id)
        if db_photo_id:         
                # review.photo_url=f'{settings.backend_url}/reviews/{review_id}/photos/{db_photo_id}/raw'
                db_review.photo_url=f'http://localhost:8081/reviews/{review_id}/photos/{db_photo_id}/raw'
                print("photo_url:",db_review.photo_url)
        else:
            db_review.photo_url=None          


        return db_review
    
    #Update  -- 본인이 작성한 글만 수정 /삭제가능
    @staticmethod
    async def update_review_by_id(db:AsyncSession, review:ReviewUpdate, review_id:int, user_id:int):
               
        db_review = await ReviewCrud.get_id(db,review_id)
        if not db_review:
            raise HTTPException(status_code=404, detail='리뷰가없습니다')
        
        if db_review.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='본인이 작성한 글만 수정가능')
        
        update_data = await ReviewCrud.update_by_id(db, review_id, review,user_id)
        await db.commit()
        await db.refresh(update_data)

        #username
        add_username(update_data)
        #like_count       
        await add_likecounts(db,update_data)
        #comment

        return update_data
        

    #Delete
    @staticmethod
    async def delete_review_by_id(db:AsyncSession, user_id:int ,review_id:int):
        db_review = await ReviewCrud.get_id(db,review_id)

        if not db_review:
            raise HTTPException(status_code=404, detail='리뷰없음')
        
        if db_review.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='본인이 작성한 글만 삭제가능')

        deleted_review = await ReviewCrud.delete_by_id(db,review_id)
        if deleted_review:            
            await db.flush()            
        return {"detail": "리뷰삭제됨"}

#좋아요(Like)
class LikeService:
    # 좋아요 토글 - 한 게시글당 한번
    @staticmethod
    async def toggle(db:AsyncSession, user_id:Optional[int], review_id:int):
        if await LikeCrud.exists(db,user_id,review_id):
            await LikeCrud.delete_id(db,user_id,review_id)
            await db.flush()
            liked = False
        else:
            await LikeCrud.create(db,user_id,review_id)
            await db.flush()
            liked = True
        
        count = await LikeCrud.count_by_review(db,review_id)
        return LikeResponse(review_id=review_id,like_count=count,liked=liked)
                             #like_count = 좋아요 갯수, liked= 로그인한 유저 좋아요 토글
    #로그인 안해도 조회
    @staticmethod 
    async def count_likes(db:AsyncSession, review_id:int, user_id:int|None=None):        
        count = await LikeCrud.count_by_review(db,review_id)
        liked=False
       
        if user_id:
            liked = await LikeCrud.exists(db,user_id,review_id)
       
        return LikeResponse(review_id=review_id,like_count=count,liked=liked)
                             
