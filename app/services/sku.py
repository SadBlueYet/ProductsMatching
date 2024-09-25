from typing import Optional
from uuid import UUID

from reposiroties import SKURepository


class SKUService:
    def __init__(self, repository: SKURepository) -> None:
        self.repository: SKURepository = repository

    def add_one(self, product: dict) -> Optional[UUID]:
        return self.repository.add_one(product)

    def get_all(self, filter_by: dict) -> list[dict]:
        return self.repository.get_all(filter_by)
