from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    name: str
    id: int

class HotelPATCH(BaseModel):
    new_title: str | None = Field(None, description="новый заголовок"),
    new_name: str | None = Field(None, description="новое имя")
