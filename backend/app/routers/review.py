from fastapi import APIRouter, Depends, Query, UploadFile, File,Form
from app.db.database import get_db
from app.db.schema.review import ReviewCreate, ReviewRead, ReviewUpdate
from app.services import ReviewService,PhotoService
from app.routers.user import Auth_Dependency, get_current_user
from app.services.review import get_current_user_id
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

router = APIRouter(prefix='/reviews',tags=['Review'])
#pydantic 의존성으로 파라미터 간소화
def as_form(
    trip_id:int,
    title: str = Form(...),
    content: str = Form(...),
    rating: int = Form(...,ge=1,le=5)
) -> ReviewCreate:
    return ReviewCreate(title=title, content=content, rating=rating,trip_id=trip_id)

# 작성한 여행계획에서 id를 가져올건지 (request body)
#Create
@router.post('/')
async def create_review(trip_id:int,                        
                        review_data:ReviewCreate=Depends(as_form),
                        db:AsyncSession=Depends(get_db),
                        current_user=Depends(get_current_user),
                        file:UploadFile=File(None)
                        ):
    # 현재 로그인한 유저의 User.id
    user_id = current_user.id
    db_review = await ReviewService.create(db,review_data,user_id,trip_id)
   
    if file is not None:    
        print("file",file)                    
        review_id=db_review.id
        print("photo.review_id",review_id)
        await PhotoService.create_image(db,review_id,user_id,file)

    return {"review_data":db_review,"photo":file}

#Read
#리뷰리스트
@router.get('/', response_model=list[ReviewRead])
async def review_list(trip_id:int|None=None,
                       db:AsyncSession=Depends(get_db),
                       serach:str|None=Query(None,min_length=1),
                       limit:int = Query(100,ge=1),
                       offset:int = Query(0,ge=0)):
    try:
        return await ReviewService.get_all_review( db=db,
                                               trip_id=trip_id,
                                               search=serach,
                                               limit=limit,
                                               offset=offset)
    except Exception as e:
        raise e
   
#상세보기
@router.get('/{review_id}', response_model=ReviewRead)
async def read_review(review_id:int,db:AsyncSession=Depends(get_db)):
    result = await ReviewService.get_review(db,review_id)
    return result

#Update
@router.put('/{review_id}', response_model=ReviewUpdate)
async def update_review(review_id:int, 
                        review:ReviewUpdate,
                        user_id:int = Depends(get_current_user_id),
                        db:AsyncSession=Depends(get_db)
                        ):
    return await ReviewService.update_review_by_id(db,review,review_id,user_id)    

#delete
@router.delete('/{review_id}')
async def delete_review_by_id(review_id:int,user_id:int =Depends(get_current_user_id),db:AsyncSession=Depends(get_db)):
    db_review = await ReviewService.delete_review_by_id(db,user_id,review_id)

    if db_review:
        return {'msg':'리뷰삭제왼료'}         