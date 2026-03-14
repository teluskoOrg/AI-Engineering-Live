import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session
from langchain_core.documents import Document

from models import Order, OrderItem, Product
from schemas import OrderRequest, OrderResponse, OrderItemResponse
from config.vector_store import vector_store


def _delete_from_vector_store_by_product(product_id: int):
    collection = vector_store._collection
    results = collection.get(where={"productId": str(product_id)})
    if results["ids"]:
        vector_store.delete(ids=results["ids"])


def place_order(db: Session, request: OrderRequest) -> OrderResponse:
    order_id = "ORD" + uuid.uuid4().hex[:10].upper()

    order = Order(
        order_id=order_id,
        customer_name=request.customer_name,
        email=request.email,
        order_date=date.today(),
        status="PLACED"
    )
    db.add(order)
    db.flush()

    created_items = []

    for item_req in request.items:
        product = db.query(Product).filter(Product.id == item_req.product_id).first()
        if not product:
            raise ValueError(f"Product not found: {item_req.product_id}")

        if product.stock_quantity < item_req.quantity:
            raise ValueError(f"Insufficient stock for: {product.name}")

        product.stock_quantity -= item_req.quantity

        _delete_from_vector_store_by_product(product.id)
        updated_doc = Document(
            page_content=f"""
Product Name: {product.name}
Description: {product.description}
Brand: {product.brand}
Category: {product.category}
Price: {float(product.price):.2f}
Available: {product.product_available}
Stock: {product.stock_quantity}
""".strip(),
            metadata={"productId": str(product.id)}
        )
        vector_store.add_documents([updated_doc], ids=[str(uuid.uuid4())])

        total = product.price * Decimal(item_req.quantity)
        order_item = OrderItem(
            product_id=product.id,
            quantity=item_req.quantity,
            total_price=total,
            order_fk=order.id
        )
        db.add(order_item)
        created_items.append((product, order_item))

    db.commit()
    db.refresh(order)

    # Index order in vector store
    content = (
        f"Order ID: {order.order_id}\n"
        f"Customer: {order.customer_name}\n"
        f"Email: {order.email}\n"
        f"Status: {order.status}\nProducts:\n"
    )
    for product, item in created_items:
        content += f"- {product.name} x {item.quantity} = {item.total_price}\n"

    order_doc = Document(page_content=content, metadata={"orderId": order.order_id})
    vector_store.add_documents([order_doc], ids=[str(uuid.uuid4())])

    item_responses = [
        OrderItemResponse(
            product_name=product.name,
            quantity=item.quantity,
            total_price=item.total_price
        )
        for product, item in created_items
    ]

    return OrderResponse(
        order_id=order.order_id,
        customer_name=order.customer_name,
        email=order.email,
        status=order.status,
        order_date=order.order_date,
        items=item_responses
    )


def get_all_orders(db: Session):
    orders = db.query(Order).all()
    result = []

    for order in orders:
        item_responses = []
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            item_responses.append(OrderItemResponse(
                product_name=product.name if product else f"Deleted Product #{item.product_id}",
                quantity=item.quantity,
                total_price=item.total_price
            ))

        result.append(OrderResponse(
            order_id=order.order_id,
            customer_name=order.customer_name,
            email=order.email,
            status=order.status,
            order_date=order.order_date,
            items=item_responses
        ))

    return result
