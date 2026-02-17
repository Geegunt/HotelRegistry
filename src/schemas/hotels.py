from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    location: str


class HotelPATCH(BaseModel):
    new_title: str | None = Field(None, description="новый заголовок"),
    location: str | None = Field(None, description="новое имя")