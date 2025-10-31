from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Comment
from app.db.schema.comment import CommentCreate, CommentUpdate, CommentRead
from app.db.crud import CommentCrud
from sqlalchemy import select
from typing import Optional

# username join :relationship
def add_username(comment:Comment):    
    if comment.users:
        comment.username = comment.users.username
    else:
        raise HTTPException(status_code=404,detail='작성자 정보 없음')
    return comment

class CommentService:
    #Create
    @staticmethod
    async def create(db:AsyncSession, 
                     comment_data:CommentCreate, 
                     user_id:int,
                     review_id:int):
        try:
            db_comment = await CommentCrud.create(db, comment_data,user_id,review_id)

            # await db.commit()
            add_username(db_comment)
            await db.refresh(db_comment)
            return db_comment
        except Exception:
            raise HTTPException(404, detail='없는 리뷰id')
    
    #Read    
    #trip id에 해당하는 list조회(R) 
    @staticmethod
    async def get_all_comment(db:AsyncSession,
                      review_id:int,
                      search:Optional[str]=None,
                      limit:int=10,
                      offset:int = 0):
        db_comment = await CommentCrud.get_all(db,review_id,search,limit,offset)
        if not db_comment:
            return []
        for comment in db_comment:
            add_username(comment)
        
        return db_comment
    
    @staticmethod
    async def get_id(db: AsyncSession, comment_id: int):
        db_comment = await CommentCrud.get_id(db, comment_id)
        if not db_comment:
            raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다")
        if not db_comment.users:
            raise HTTPException(status_code=404, detail='작성자 정보 없음')
        
        #username
        add_username(db_comment)

        return db_comment

    #Update
    @staticmethod
    async def update_comment_by_id(db:AsyncSession, comment:CommentUpdate, comment_id:int, user_id:int):               
        db_comment = await CommentCrud.get_id(db,comment_id)

        if not db_comment:
            raise HTTPException(status_code=404, detail='댓글이 없습니다')
        #권한체크
        if db_comment.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='본인이 작성한 댓글만 수정가능')
        
        update_data = await CommentCrud.update_by_id(db, comment,comment_id,user_id)
        # await db.commit()
        await db.refresh(update_data)
        return update_data        

    #Delete
    @staticmethod
    async def delete_comment_by_id(db:AsyncSession, comment_id:int,user_id:int):
        db_comment = await db.execute(select(Comment).where(Comment.id==comment_id))
        comment = db_comment.scalar_one_or_none()        

        if not comment:
            raise HTTPException(status_code=404, detail='댓글없음')
        
        if comment.user_id !=user_id:
            raise HTTPException(status_code=403, detail='삭제권한없음')

        deleted_comment = await CommentCrud.delete_by_id(db,comment_id,user_id)
        if deleted_comment:            
            await db.flush()            
            return deleted_comment