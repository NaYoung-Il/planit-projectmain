from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.schema.review import LikeResponse 
from app.services import LikeService
from app.services.review import get_current_user_id

router = APIRouter(prefix='/reviews',tags=['Like'])

#로그인한 유저 좋아요 토글 요청 + 좋아요 갯수
@router.post('/{review_id}/likes', response_model=LikeResponse)
async def toggle_like(review_id:int,
                      user_id:int=Depends(get_current_user_id),
                      db:AsyncSession=Depends(get_db)):
    return await LikeService.toggle(db,user_id,review_id)

#페이지 로드시 좋아요 수 노출
@router.get('/{review_id}/likes', response_model=LikeResponse)
async def get_likes(review_id:int,
                    user_id:int|None = Depends(get_current_user_id),
                    db:AsyncSession=Depends(get_db)):
    return await LikeService.count_likes(db,review_id,user_id)
