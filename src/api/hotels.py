from fastapi import APIRouter, Query, Body
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH
from sqlalchemy import insert, select, func

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="получение списка отелей/отеля")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес")
 ):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).like(f"%{location.lower()}%"))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).like(f"%{title.lower()}%"))

        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
         )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await session.execute(query)

        hotels = result.scalars().all()
        print(type(hotels), hotels)
        return hotels

    # if pagination.page and pagination.per_page:
    #     return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]



@router.post("", summary="создание нового отеля")
async def create_hotel(
        hotel_data:
        Hotel = Body(openapi_examples={
            "1": {"summary": "Сочи", "value":  {
            "title": "Отель Сочи 5 звезд у моря",
            "location": "Ул. Моряка, 1"
        }}, "2": {"summary": "Дубай", "value":  {
            "title": "Отель Дубай у фонтана",
            "location": "Ул. Жары, 52"
        }},
})
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}

@router.delete("/{hotel_id}", summary="удаление отеля")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@router.put("/{hotel_id}", summary="полное изменение отеля")
def put_change_hotel(old_id: int, hotel_data: Hotel = Body()):
    global hotels
    if hotel_data.title and hotel_data.id and hotel_data.name:
        hotels[old_id - 1]["id"] = hotel_data.id
        hotels[old_id - 1]["title"] = hotel_data.title
        hotels[old_id - 1]["name"] = hotel_data.name

@router.patch("/{hotel_id}", summary="частиное изменение отеля",
           description="Здесь можно отсавить полное описание ручки")
def patch_change_hotel(old_id: int,
                       hotel_data: HotelPATCH):
    global hotels
    if hotel_data.new_title != 'string' and hotel_data.new_title:
        hotels[old_id - 1]["title"] = hotel_data.new_title
    if hotel_data.new_name != 'string' and hotel_data.new_name:
        hotels[old_id - 1]["name"] = hotel_data.new_name