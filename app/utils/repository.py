from abc import ABC, abstractmethod
from typing import Optional, Type
from uuid import UUID

from database import session_local
from sqlalchemy import insert
from sqlalchemy.exc import DataError
from sqlalchemy.orm import DeclarativeMeta


class AbstractRepository(ABC):

    @abstractmethod
    def add_one(self, data: dict) -> Optional[UUID]:
        pass


class SQLAlchemyRepsitory(AbstractRepository):
    model: Type[DeclarativeMeta]

    def add_one(self, data: dict) -> Optional[UUID]:
        with session_local() as session:
            try:
                stmt = insert(self.model).values(**data).returning(self.model.uuid)
                res = session.execute(stmt)
                session.commit()
                return res.scalar()
            except DataError:
                return None
