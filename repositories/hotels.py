from sqlalchemy import select, func
from sqlalchemy.sql.expression import insert, update, delete

from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from pydantic import BaseModel


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ):
        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))

        query = (
            query
            .limit(limit)
            .offset(offset)
         )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return result.scalars().all()

    async def add(
            self,
            data: BaseModel,
    ):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        update_stmt = ((update(self.model)
                       .filter_by(**filter_by)
                        .values(**data.model_dump(exclude_unset=True)))
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
