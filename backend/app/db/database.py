from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.settings import settings


async_engine = create_async_engine(settings.database_url, echo=False)


AsyncsessionLocal = sessionmaker(
    autocommit = False, autoflush=False, bind=async_engine, class_=AsyncSession
)

Base=declarative_base()


# 수정된 get_db 함수
async def get_db():
    async with AsyncsessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback() # 오류 발생 시 DB 작업을 취소합니다.
            raise                # 오류를 다시 발생시켜 FastAPI가 인지하게 합니다.

#DB연결 경로 확인 (추후삭제)
print("DB URL:", settings.database_url)