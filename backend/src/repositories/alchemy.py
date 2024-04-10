from pydantic import BaseModel
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.base import AbstractRepo
from typing import List


class SqlAlchemyRepo(AbstractRepo):
    model = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def delete_by_id(self, model_id: int) -> None:
        stmt = delete(self.model).where(id=model_id)
        await self.session.execute(stmt)

    async def find_one(self, **filter_by) -> BaseModel:
        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        result = result.scalar_one_or_none()
        if result:
            result = result.to_read_model()
        return result

    async def find_all(self, **filter_by) -> List[BaseModel]:
        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        result = [row[0].to_read_model() for row in result.all()]
        return result

    async def add_one(self, **data) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()
