from datetime import date

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking

class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking
    def total_cost(self,
                   price: int,
                   date_from: date,
                   date_to: date
                   ) -> int:
        return price * (date_to - date_from).days

