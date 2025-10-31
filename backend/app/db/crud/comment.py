from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Comment
from app.db.schema.comment import CommentCreate, CommentUpdate, CommentRead
from sqlalchemy import select, or_, desc, func
from typing import Optional

class CommentCrud:
    @staticmethod
    async def create(db:AsyncSession, 
                    comment_data:CommentCreate,
                    user_id:int,
                    review_id:int):

        comment_dict = comment_data.model_dump()
        comment_dict['user_id'] = user_id
        comment_dict['review_id'] = review_id
        new_comment = Comment(**comment_dict)
        db.add(new_comment)
        await db.flush()
        return new_comment
    
    @staticmethod
    async def get_id(db:AsyncSession, comment_id:int) -> Optional[Comment]:
        return await db.get(Comment, comment_id)

    @staticmethod
    async def get_all(db:AsyncSession,
                      review_id:int, 
                      search:Optional[str]=None,                     
                      limit:int=10,
                      offset:int = 0
                      ):
        #데이터선택
        query = select(Comment).where(Comment.review_id == review_id)
        
        #페이지네이션
        query = query.limit(limit).offset(offset)

        result = await db.execute(query)
        return result.scalars().all() #rows=result.scalars().all()
    
    #Update(review_id)
    @staticmethod
    async def update_by_id(db:AsyncSession, comment:CommentUpdate, comment_id:int, user_id:int) -> Optional[Comment]:
        db_comment = await db.get(Comment, comment_id)
        if db_comment and db_comment.user_id == user_id:
            update_comment = comment.model_dump(exclude_unset=True) 
            for field, value in update_comment.items():
                setattr(db_comment, field, value)
            await db.flush()
            return db_comment
        return None
    
    #Delete
    @staticmethod
    async def delete_by_id(db:AsyncSession, comment_id:int, user_id:int) -> bool:
        comment = await db.get(Comment, comment_id)
        if comment and comment.user_id == user_id:
            await db.delete(comment)
            await db.flush()
            return True
        return False