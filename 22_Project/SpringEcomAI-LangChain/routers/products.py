import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session

from database import get_db
from schemas import ProductResponse
import services.product_service as product_service

router = APIRouter(prefix="/api", tags=["products"])


async def _get_form_data(request: Request):
    """Read product JSON and optional image from raw multipart form."""
    form = await request.form()

    # Parse product JSON (sent as blob or string)
    product_field = form.get("product")
    if hasattr(product_field, "read"):
        product_data = json.loads(await product_field.read())
    else:
        product_data = json.loads(product_field)

    # Parse image — React sends "null" string when no image selected
    image_bytes = image_name = image_type = None
    image_field = form.get("imageFile")
    if image_field and not isinstance(image_field, str) and hasattr(image_field, "read"):
        if image_field.filename not in (None, "", "null", "undefined"):
            image_bytes = await image_field.read()
            image_name = image_field.filename
            image_type = image_field.content_type

    return product_data, image_bytes, image_name, image_type


@router.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return product_service.get_all_products(db)


@router.get("/product/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/product/{product_id}/image")
def get_product_image(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product_by_id(db, product_id)
    if not product or not product.product_image:
        raise HTTPException(status_code=404, detail="Image not found")
    return Response(content=product.product_image, media_type=product.image_type or "image/jpeg")


@router.post("/product", response_model=ProductResponse)
async def add_product(request: Request, db: Session = Depends(get_db)):
    product_data, image_bytes, image_name, image_type = await _get_form_data(request)
    return product_service.add_or_update_product(db, product_data, image_bytes, image_name, image_type)


@router.put("/product/{product_id}")
async def update_product(product_id: int, request: Request, db: Session = Depends(get_db)):
    product_data, image_bytes, image_name, image_type = await _get_form_data(request)
    product_data["id"] = product_id
    product_service.add_or_update_product(db, product_data, image_bytes, image_name, image_type)
    return {"message": "Updated"}


@router.delete("/product/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_service.delete_product(db, product_id)
    return {"message": "Deleted"}


@router.post("/product/generate-description")
def generate_description(name: str, category: str):
    return product_service.generate_description(name, category)


@router.post("/product/generate-image")
def generate_image_endpoint(name: str, category: str, description: str):
    image_bytes = product_service.generate_product_image(name, category, description)
    return Response(content=image_bytes, media_type="image/png")


@router.get("/products/smart-search", response_model=List[ProductResponse])
def smart_search(query: str, db: Session = Depends(get_db)):
    return product_service.semantic_search_products(db, query)