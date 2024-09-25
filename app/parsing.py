from collections.abc import Generator

from lxml import etree


class Parser:
    xml_file: str

    def __init__(self, xml_file: str) -> None:
        self.xml_file = xml_file

    def parsing_xml(self) -> Generator:
        context = etree.iterparse(self.xml_file, events=("end",), tag="offer")
        for _, elem in context:
            yield elem
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

    def extract_from_offer_tag(self, elem) -> dict:
        category_path = self.find_and_build_path(elem.findtext("categoryId"))
        return {
            "marketplace_id": elem.findtext("marketplaceId"),
            "product_id": elem.get("id"),
            "title": elem.findtext("name"),
            "description": elem.findtext("description"),
            "brand": elem.findtext("vendor"),
            "seller_id": elem.findtext("sellerId"),
            "seller_name": elem.findtext("sellerName"),
            "first_image_url": elem.findtext("picture"),
            "category_id": elem.findtext("categoryId"),
            "category_lvl_1": (
                None if not category_path else category_path.split("/")[0]
            ),
            "category_lvl_2": (
                None if not category_path else category_path.split("/")[1]
            ),
            "category_lvl_3": (
                None if not category_path else category_path.split("/")[2]
            ),
            "category_remaining": (
                None if not category_path else "/".join(category_path.split("/")[3:])
            ),
            "features": elem.findtext("params"),
            "rating_count": elem.findtext("raitingCount"),
            "rating_value": elem.findtext("raitingValue"),
            "price_before_discounts": elem.findtext("oldprice"),
            "discount": elem.findtext("discount"),
            "bonuses": elem.findtext("bonuses"),
            "sales": elem.findtext("sales"),
            "currency": elem.findtext("currencyId"),
            "barcode": elem.findtext("barcode"),
        }

    def find_category_by_id_in_stream(self, category_id: str):
        context = etree.iterparse(self.xml_file, events=("end",), tag="category")

        for _, elem in context:
            if elem.get("id") == category_id:
                return elem
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        return None

    def build_category_path_in_stream(self, category_element):
        category_name = category_element.text
        parent_id = category_element.get("parentId")

        if parent_id:
            parent_category = self.find_category_by_id_in_stream(parent_id)
            if parent_category is not None:
                return (
                    self.build_category_path_in_stream(parent_category)
                    + "/"
                    + category_name
                )

        return category_name

    def find_and_build_path(self, category_id: str):
        context = etree.iterparse(self.xml_file, events=("end",), tag="category")

        for _, elem in context:
            if elem.get("id") == category_id:
                full_path = self.build_category_path_in_stream(elem)
                return full_path
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

        return None
