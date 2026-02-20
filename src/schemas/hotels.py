from pydantic import BaseModel, Field


class HotelAdd(BaseModel):
    title: str
    location: str

class Hotel(HotelAdd):
    id: int

class HotelPATCH(BaseModel):
    new_title: str | None = Field(None, description="новый заголовок"),
    location: str | None = Field(None, description="новое имя")