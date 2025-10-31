from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger, ForeignKey
from typing import Optional

class Place(Base):
    __tablename__ = "places"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True) 
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False) 
    place_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  
    type_id: Mapped[int] = mapped_column(ForeignKey("travel_types.id"), nullable=False) 
    place_intro: Mapped[Optional[str]] = mapped_column(String(4000), nullable=True)  # 수정됨: LONGTEXT -> String(4000)
    is_popular: Mapped[Optional[bool]] = mapped_column(nullable=True, default=False)  # 추가됨: 추천 장소 여부

    city = relationship("City", back_populates="place")
    travel_types = relationship("TravelType", back_populates="place")
    schedule = relationship("Schedule", back_populates="place")

# CREATE TABLE places (
#     id BIGINT PRIMARY KEY AUTO_INCREMENT,
#     city_id BIGINT NOT NULL,
#     place_name VARCHAR(255),
#     type_id BIGINT NOT NULL,
#     -- user_id BIGINT,                                -- 추가됨: 기존 popular의 user_id 반영
#     place_intro LONGTEXT,                          -- 추가됨: 기존 popular의 city_intro 반영
#     is_popular BOOLEAN DEFAULT FALSE,              -- 추가됨: 추천 여부 표시
#     FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE,
#     FOREIGN KEY (type_id) REFERENCES travel_types(id) ON DELETE CASCADE
#     -- FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE -- popular 기능 흡수
# );