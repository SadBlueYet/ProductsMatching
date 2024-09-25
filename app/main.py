from uuid import UUID

from config import FILE_NAME
from database import engine
from dependencies import SKU_service
from matching import Matcher
from models import Base
from parsing import Parser
from services import SKUService

CHUNK_SIZE = 1000


def indexing(products: list[dict], matcher: Matcher) -> None:
    prepared_products = matcher.data_preparation(products)
    matcher.indexing(prepared_products)


def matching(products: list[dict], matcher: Matcher, service: SKUService) -> None:
    for i in range(len(products)):
        matched_products = matcher.matching(products[i])
        if matched_products is not None:
            update_similar_scu(service, products[i], matched_products)


def update_similar_scu(
    service: SKUService, product: dict, match_products: list[dict]
) -> None:
    service.repository.update_one(
        product["uuid"],
        {"similar_sku": [UUID(i["uuid"]) for i in match_products]},
    )


def main():
    Base.metadata.create_all(engine)
    parser = Parser(FILE_NAME)
    matcher = Matcher()
    service = SKU_service()
    counter = 0

    for elem in parser.parsing_xml():
        product = parser.extract_from_offer_tag(elem)
        service.add_one(product)
        counter += 1

        if counter % CHUNK_SIZE == 0:
            products = service.repository.get_products_by_limit(
                counter - CHUNK_SIZE, counter
            )

            indexing(products, matcher)
            matching(products, matcher, service)

            print(f"Обработано {counter}: файлов")
        if counter % 2000 == 0:
            matcher.delete_index()


if __name__ == "__main__":
    main()
