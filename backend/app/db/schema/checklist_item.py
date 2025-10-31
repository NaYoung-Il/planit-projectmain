from pydantic import BaseModel, Field
from typing import Optional

class ChecklistItemBase(BaseModel):
    item_name: str = Field(..., max_length=255)
    is_checked: bool = False

class ChecklistItemCreate(ChecklistItemBase):
    trip_id: int

class ChecklistItemUpdate(BaseModel):
    item_name: Optional[str] = Field(None, max_length=255)
    is_checked: Optional[bool] = None

class ChecklistItemInDB(ChecklistItemBase):
    id: int
    trip_id: int

    class Config:
        from_attributes = True