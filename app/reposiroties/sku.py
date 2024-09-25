from typing import Optional, Type
from uuid import UUID

from database import session_local
from models import SKU
from sqlalchemy import select, update
from utils import SQLAlchemyRepsitory


class SKURepository(SQLAlchemyRepsitory):
    model: Type[SKU] = SKU

    def get_products_by_limit(
        self, offset: int = 0, batch_size: int = 10000
    ) -> list[dict]:
        with session_local() as session:
            results = (
                session.execute(select(self.model).limit(batch_size).offset(offset))
                .scalars()
                .all()
            )
            return [res.to_read_model() for res in results]

    def update_one(self, uuid: UUID, data: dict) -> Optional[UUID]:
        with session_local() as session:
            try:
                stmt = update(self.model).where(self.model.uuid == uuid).values(**data)
                session.execute(stmt)
                session.commit()
                return uuid
            except Exception:
                session.rollback()
                return None

    def get_all(self, filter_by: dict) -> list[dict]:
        with session_local() as session:
            results = (
                session.execute(select(self.model).filter_by(**filter_by))
                .scalars()
                .all()
            )
            return [res.to_read_model() for res in results]
