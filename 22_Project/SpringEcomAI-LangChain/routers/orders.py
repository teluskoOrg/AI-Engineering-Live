from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import OrderRequest
import services.order_service as order_service

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("/place")
def place_order(request: OrderRequest, db: Session = Depends(get_db)):
    try:
        return order_service.place_order(db, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
def get_all_orders(db: Session = Depends(get_db)):
    return order_service.get_all_orders(db)
