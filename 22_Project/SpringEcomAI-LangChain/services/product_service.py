from decimal import Decimal
import base64
import uuid
import json
import re
from pathlib import Path

from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document

from models import Product
from config.vector_store import vector_store
from services.ai_image_service import generate_image

llm = ChatOpenAI(model="gpt-4o")

SEARCH_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "product-search-prompt.st"


def _load_search_prompt(context: str, user_query: str) -> str:
    template = SEARCH_PROMPT_PATH.read_text(encoding="utf-8")
    return template.replace("{userQuery}", user_query).replace("{context}", context)


def _to_snake_case(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def _product_to_text(product: Product) -> str:
    return f"""
Product Name: {product.name}
Description: {product.description}
Brand: {product.brand}
Category: {product.category}
Price: {float(product.price):.2f}
Release Date: {product.release_date}
Available: {product.product_available}
Stock: {product.stock_quantity}
""".strip()


def _delete_from_vector_store(product_id: int):
    collection = vector_store._collection
    results = collection.get(where={"productId": str(product_id)})
    if results["ids"]:
        vector_store.delete(ids=results["ids"])


def _index_product(product: Product):
    doc = Document(
        page_content=_product_to_text(product),
        metadata={"productId": str(product.id)}
    )
    vector_store.add_documents([doc], ids=[str(uuid.uuid4())])


def _convert_types(data: dict) -> dict:
    """Convert string values from React to proper Python types — same as Spring Boot Jackson."""

    data.pop("product_image", None)
    data.pop("image_name", None)
    data.pop("image_type", None)

    if "release_date" in data and isinstance(data["release_date"], str):
        try:
            from datetime import datetime
            data["release_date"] = datetime.strptime(data["release_date"], "%Y-%m-%d").date()
        except (ValueError, TypeError):
            data["release_date"] = None

    if "price" in data and data["price"] is not None:
        data["price"] = Decimal(str(data["price"]))

    if "stock_quantity" in data and data["stock_quantity"] is not None:
        data["stock_quantity"] = int(data["stock_quantity"])

    return data


def get_all_products(db: Session):
    return db.query(Product).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def add_or_update_product(
    db: Session,
    product_data: dict,
    image_bytes: bytes = None,
    image_name: str = None,
    image_type: str = None
) -> Product:
    product_data = {_to_snake_case(k): v for k, v in product_data.items()}

    product_data = _convert_types(product_data)

    product_id = product_data.get("id")

    if product_id:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            product = Product()
    else:
        product = Product()

    for key, value in product_data.items():
        if hasattr(product, key) and key != "id":
            setattr(product, key, value)

    if image_bytes:
        product.image_name = image_name
        product.image_type = image_type
        product.product_image = image_bytes

    db.add(product)
    db.commit()
    db.refresh(product)

    _delete_from_vector_store(product.id)
    _index_product(product)

    return product


def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()


def generate_description(name: str, category: str) -> str:
    prompt = f"""
Write a concise and professional product description for an e-commerce listing.

Product Name: {name}
Category: {category}

Keep it simple, engaging, and highlight its primary features or benefits.
Avoid technical jargon and keep it customer-friendly.
Limit the description to 250 characters maximum.
""".strip()
    return llm.invoke(prompt).content


def generate_product_image(name: str, category: str, description: str) -> bytes:
    prompt = f"""
Generate a highly realistic, professional-grade e-commerce product image.

Product Details:
- Category: {category}
- Name: '{name}'
- Description: {description}

Requirements:
  - Clean white/light grey background, soft natural lighting.
  - No humans, logos, watermarks, or text.
  - Professional e-commerce style like Amazon or Flipkart.
""".strip()
    return generate_image(prompt)


def semantic_search_products(db: Session, query: str):

    all_products = db.query(Product).all()
    
    context = "\n\n".join([_product_to_text(p) + f"\nProduct ID: {p.id}" for p in all_products])

    prompt = _load_search_prompt(context, query)

    response = llm.invoke(prompt).content
    response = re.sub(r"```json|```", "", response).strip()

    products_data = json.loads(response)
    product_ids = [int(p["id"]) for p in products_data if int(p.get("id", 0)) > 0]

    return db.query(Product).filter(Product.id.in_(product_ids)).all()