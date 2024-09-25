from typing import Optional

from config import ELASTIC_HOST, ELASTIC_PORT
from elasticsearch import Elasticsearch, helpers


class Matcher:
    client: Elasticsearch

    def __init__(self) -> None:
        self.client = Elasticsearch(f"http://{ELASTIC_HOST}:{ELASTIC_PORT}")

    def data_preparation(self, data: list[dict]) -> list[dict]:
        actions = []
        for row in data:
            actions.append(
                {
                    "uuid": row["uuid"],
                    "product_id": row["product_id"],
                    "title": row["title"],
                    "description": row["description"],
                    "brand": row["brand"],
                    "price_after_discounts": row["price_after_discounts"],
                    "category_lvl_3": row["category_lvl_3"],
                }
            )
        return actions

    def indexing(self, data: list[dict]) -> None:
        actions = [
            {"_index": "products", "_id": row["uuid"], "_source": row} for row in data
        ]
        helpers.bulk(self.client, actions)

    def matching(self, data: dict) -> Optional[list[dict]]:
        try:
            match_products = self.client.search(
                index="products",
                query={
                    "bool": {
                        "must": [
                            {"match": {"category_lvl_3": data["category_lvl_3"]}},
                            {"match": {"brand": data["brand"]}},
                        ]
                    }
                },
                size=5,
            )
        except Exception:
            return None

        if match_products["hits"]["total"]["value"] > 0:
            products = []
            for hit in match_products["hits"]["hits"]:
                products.append(hit["_source"])
            return products
        else:
            return None

    def delete_index(self) -> None:
        self.client.indices.delete(index="products")
