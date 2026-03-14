from pydantic import BaseModel, ConfigDict, field_serializer
from pydantic.alias_generators import to_camel
from typing import List, Optional
from datetime import date
from decimal import Decimal
import base64

_camel_config = ConfigDict(
    from_attributes=True,
    populate_by_name=True,
    alias_generator=to_camel
)


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    brand: Optional[str] = None
    price: Decimal
    category: str
    release_date: Optional[date] = None
    product_available: bool = True
    stock_quantity: int = 0
    model_config = _camel_config


class ProductResponse(ProductBase):
    id: int
    image_name: Optional[str] = None
    image_type: Optional[str] = None
    product_image: Optional[bytes] = None

    @field_serializer("product_image")
    def serialize_image(self, value: Optional[bytes]) -> Optional[str]:
        if value is None:
            return None
        return base64.b64encode(value).decode("utf-8")


class OrderItemRequest(BaseModel):
    product_id: int
    quantity: int
    model_config = _camel_config          


class OrderRequest(BaseModel):
    customer_name: str
    email: str
    items: List[OrderItemRequest]
    model_config = _camel_config          


class OrderItemResponse(BaseModel):
    product_name: str
    quantity: int
    total_price: Decimal
    model_config = _camel_config


class OrderResponse(BaseModel):
    order_id: str
    customer_name: str
    email: str
    status: str
    order_date: date
    items: List[OrderItemResponse]
    model_config = _camel_config