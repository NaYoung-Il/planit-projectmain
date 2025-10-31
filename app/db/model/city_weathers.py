from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class CityWeather(Base):
    __tablename__ = "city_weathers"

    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), primary_key=True)  
    weather_id: Mapped[int] = mapped_column(ForeignKey("weather.id", ondelete="CASCADE"), primary_key=True)  

    city = relationship("City", back_populates="city_weathers")
    weather = relationship("Weather", back_populates="city_weathers")

# CREATE TABLE city_weathers (
#     city_id BIGINT NOT NULL,
#     weather_id BIGINT NOT NULL,
#     PRIMARY KEY (city_id, weather_id), -- 추가됨: 중복 방지 복합키
#     FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE,
#     FOREIGN KEY (weather_id) REFERENCES weather(id) ON DELETE CASCADE
#     -- 변경됨: weather와 city 직접 연결 대신, 중간 테이블을 통해 연결
# );