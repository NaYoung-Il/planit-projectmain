from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship # 관계 설정을 위해 임포트
from app.db.database import Base 

class Group(Base):
    __tablename__ = "GROUPT" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255))

    # User 모델과의 역방향 관계 설정
    # User 모델에서 group 관계에 설정한 back_populates="users"에 대응합니다.
    # uselist=True는 Group 하나에 여러 User가 연결될 수 있음(One-to-Many)을 나타냅니다.
    users = relationship("User", back_populates="group", uselist=True)