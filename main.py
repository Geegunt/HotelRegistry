from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"}
]

@app.get("/hotels", summary="получение списка отелей/отеля")
def get_hotels(
        title: str | None = Query(None, description="название отеля"),
        id: int | None = Query(None, description="Айдишник")
               ):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_

@app.post("/hotels", summary="создание нового отеля")
def create_hotel(title: str = Body(embed=True)):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title})

@app.delete("/hotels/{hotel_id}", summary="удаление отеля")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@app.put("/hotels/{hotel_id}", summary="полное изменение отеля")
def put_change_hotel(old_id: int, new_title: str, new_id: int, new_name: str):
    global hotels
    if new_title and new_id and new_name:
        hotels[old_id - 1]["id"] = new_id
        hotels[old_id - 1]["title"] = new_title
        hotels[old_id - 1]["name"] = new_name

@app.patch("/hotels/{hotel_id}", summary="частиное изменение отеля",
           description="Здесь можно отсавить полное описание ручки")
def patch_change_hotel(old_id: int, new_id: int | None = Body(None, description="новый айди"),
                       new_title: str | None = Body(None, description="новый заголовок"),
                       new_name: str | None = Body(None, description="новое имя")):
    global hotels
    if new_id != 0 and new_id:
        hotels[old_id - 1]["id"] = new_id
    if new_title != 'string' and new_title:
        hotels[old_id - 1]["title"] = new_title
    if new_name != 'string' and new_name:
        hotels[old_id - 1]["name"] = new_name


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(): ...


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

