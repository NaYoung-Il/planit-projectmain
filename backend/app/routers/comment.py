from fastapi import APIRouter, Depends, Request, Query
from app.db.database import get_db
from app.db.model import Comment
from app.db.schema.comment import CommentCreate, CommentRead, CommentUpdate
from app.services import CommentService
from app.services.review import get_current_user_id

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/reviews/{review_id}/comments',tags=['Comments'])

#로그인한 사람만 댓글작성
@router.post('/', response_model=CommentRead)
async def create_comment(review_data:CommentCreate,
                        review_id:int,
                        user_id:int = Depends(get_current_user_id),                        
                        db:AsyncSession=Depends(get_db)):
    return await CommentService.create(db,review_data,user_id,review_id)

#get_list - 댓글없으면 빈배열 반환
@router.get('/', response_model=list[CommentRead])
async def comment_list(review_id:int,
                       db:AsyncSession=Depends(get_db),
                       serach:str|None=Query(None,min_length=1),
                       limit:int = Query(10,ge=1,le=30),
                       offset:int = Query(0,ge=0)):
    return await CommentService.get_all_comment(db=db,
                                               review_id=review_id,
                                               search=serach,
                                               limit=limit,
                                               offset=offset)                                       
    
#get_comment_from_id
@router.get('/{comment_id}', response_model=CommentRead)
async def get_comment(comment_id:int,db:AsyncSession=Depends(get_db)):
    result = await CommentService.get_id(db,comment_id)    
    return result

#Update
@router.put('/{comment_id}', response_model=CommentRead)
async def update_comment(comment_id:int, 
                        comment:CommentUpdate,
                        user_id:int = Depends(get_current_user_id),
                        db:AsyncSession=Depends(get_db)
                        ):
    return await CommentService.update_comment_by_id(db,comment,comment_id,user_id)    

#delete
@router.delete('/delete/{comment_id}')
async def delete_comment_by_id(comment_id:int,
                               user_id:int=Depends(get_current_user_id),
                               db:AsyncSession=Depends(get_db)):
    db_comment = await CommentService.delete_comment_by_id(db, comment_id, user_id)
    if db_comment:
        return {'msg':'댓글 삭제완료'}
