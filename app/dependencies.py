from reposiroties import SKURepository
from services import SKUService


def SKU_service() -> SKUService:
    return SKUService(SKURepository())
