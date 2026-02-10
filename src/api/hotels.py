from fastapi import APIRouter, Query, Body
from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

@router.get("", summary="получение списка отелей/отеля")
def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        id: int | None = Query(None, description="Айдишник"),
 ):
    global hotels
    start = (pagination.page - 1) * pagination.per_page
    end = start + pagination.per_page
    return hotels[start:end]
    # hotels_ = []
    # for hotel in hotels:
    #     if id and hotel["id"] != id:
    #         continue
    #     if title and hotel["title"] != title:
    #         continue
    #     hotels_.append(hotel)
    # return hotels_


@router.post("", summary="создание нового отеля")
def create_hotel(
        hotel_data:
        Hotel = Body(openapi_examples={
            "1": {"summary": "Сочи", "value":  {
            "title": "Отель Сочи 5 звезд у моря",
            "name": "sichi_y_morya"
        }}, "2": {"summary": "Дубай", "value":  {
            "title": "Отель Дубай у фонтана",
            "name": "Fontain"
        }},
})
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })

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