import uuid

from models import Base
from sqlalchemy import (
    ARRAY,
    JSON,
    TIMESTAMP,
    UUID,
    BigInteger,
    Column,
    Float,
    Index,
    Integer,
    Text,
    UniqueConstraint,
)
from sqlalchemy.sql import func


class SKU(Base):
    __tablename__ = "sku"

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="id товара в нашей бд",
    )
    marketplace_id = Column(Integer, nullable=True, comment="id маркетплейса")
    product_id = Column(BigInteger, nullable=True, comment="id товара в маркетплейсе")
    title = Column(Text, nullable=True, comment="название товара")
    description = Column(Text, nullable=True, comment="описание товара")
    brand = Column(Text, nullable=True)
    seller_id = Column(Integer, nullable=True)
    seller_name = Column(Text, nullable=True)
    first_image_url = Column(Text, nullable=True)
    category_id = Column(Integer, nullable=True, comment="id категории товара")
    category_lvl_1 = Column(
        Text, nullable=True, comment="Первая часть категории товара"
    )
    category_lvl_2 = Column(
        Text, nullable=True, comment="Вторая часть категории товара"
    )
    category_lvl_3 = Column(
        Text, nullable=True, comment="Третья часть категории товара"
    )
    category_remaining = Column(Text, nullable=True, comment="Остаток категории товара")
    features = Column(JSON, nullable=True, comment="Характеристики товара")
    rating_count = Column(Integer, nullable=True, comment="Кол-во отзывов о товаре")
    rating_value = Column(Float, nullable=True, comment="Рейтинг товара (0-5)")
    price_before_discounts = Column(Float, nullable=True)
    discount = Column(Float, nullable=True)
    price_after_discounts = Column(Float, nullable=True)
    bonuses = Column(Integer, nullable=True)
    sales = Column(Integer, nullable=True)
    inserted_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    currency = Column(Text, nullable=True)
    barcode = Column(BigInteger, nullable=True, comment="Штрихкод")
    similar_sku = Column(ARRAY(UUID(as_uuid=True)), nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "marketplace_id",
            "product_id",
            name="sku_marketplace_id_product_id_uindex",
        ),
        UniqueConstraint("uuid", name="sku_uuid_uindex"),
        Index("sku_brand_index", "brand"),
    )

    def to_read_model(self):
        return {
            "uuid": self.uuid,
            "marketplace_id": self.marketplace_id,
            "product_id": self.product_id,
            "title": self.title,
            "description": self.description,
            "brand": self.brand,
            "seller_id": self.seller_id,
            "seller_name": self.seller_name,
            "first_image_url": self.first_image_url,
            "category_id": self.category_id,
            "category_lvl_1": self.category_lvl_1,
            "category_lvl_2": self.category_lvl_2,
            "category_lvl_3": self.category_lvl_3,
            "category_remaining": self.category_remaining,
            "features": self.features,
            "rating_count": self.rating_count,
            "rating_value": self.rating_value,
            "price_before_discounts": self.price_before_discounts,
            "discount": self.discount,
            "price_after_discounts": self.price_after_discounts,
            "bonuses": self.bonuses,
            "sales": self.sales,
            "inserted_at": self.inserted_at,
            "updated_at": self.updated_at,
            "currency": self.currency,
            "barcode": self.barcode,
            "similar_sku": self.similar_sku,
        }
