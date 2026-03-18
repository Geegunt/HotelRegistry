from datetime import date

from fastapi import APIRouter, Query, Body
from src.api.dependencies import PaginationDep, DBDep, UserIdDep

from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.get("")
async def get_bookings(
        db: DBDep,
):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(
        db: DBDep,
        user_id: UserIdDep,

):
    return await db.bookings.get_filtered(user_id=user_id)

@router.post("")
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingAddRequest = Body(),
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    price_room = room.price
    booking_create = BookingAdd(
        room_id=booking_data.room_id,
        user_id=user_id,
        date_from=booking_data.date_from,
        date_to=booking_data.date_to,
        price=price_room
    )

    booking = await db.bookings.add(booking_create)
    await db.commit()
    return {"status": "OK", "data": booking}




