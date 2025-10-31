from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger
from typing import Optional

class TravelType(Base):
    __tablename__ = "travel_types"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True) 
    type_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  

    place = relationship("Place", back_populates="travel_types")

# CREATE TABLE travel_types (
#     id BIGINT PRIMARY KEY AUTO_INCREMENT,
#     type_name VARCHAR(255)
# );