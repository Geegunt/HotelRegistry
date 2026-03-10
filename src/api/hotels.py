from fastapi import APIRouter, Query, Body

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import Hotel, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="получение списка отелей/отеля")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес")
 ):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page or 5,
        offset=per_page * (pagination.page - 1)
    )

@router.get("/{hotel_id}")
async def get_hotel(
        db: DBDep,
        hotel_id: int):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("", summary="создание нового отеля")
async def create_hotel(
        db: DBDep,
        hotel_data:
        HotelAdd = Body(openapi_examples={
            "1": {"summary": "Сочи", "value":  {
            "title": "Отель Сочи 5 звезд у моря",
            "location": "Ул. Моряка, 1"
        }}, "2": {"summary": "Дубай", "value":  {
            "title": "Отель Дубай у фонтана",
            "location": "Ул. Жары, 52"
        }},
})
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}

@router.delete("/{hotel_id}", summary="удаление отеля")
async def delete_hotel(
        db: DBDep,
        hotel_id: int,
                       ):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.put("/{hotel_id}", summary="полное изменение отеля")
async def put_change_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: Hotel = Body(),
):
    await db.hotels.edit(data=hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.patch("/{hotel_id}", summary="частиное изменение отеля",
           description="Здесь можно отсавить полное описание ручки")
async def patch_change_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelAdd):
    await db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}