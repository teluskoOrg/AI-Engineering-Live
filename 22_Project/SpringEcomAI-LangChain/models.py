from sqlalchemy import Column, Integer, String, Boolean, Date, LargeBinary, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    brand = Column(String)
    price = Column(Numeric(10, 2))
    category = Column(String)
    release_date = Column(Date, nullable=True)
    product_available = Column(Boolean, default=True)
    stock_quantity = Column(Integer, default=0)
    image_name = Column(String, nullable=True)
    image_type = Column(String, nullable=True)
    product_image = Column(LargeBinary, nullable=True)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True)
    customer_name = Column(String)
    email = Column(String)
    status = Column(String)
    order_date = Column(Date)
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    total_price = Column(Numeric(10, 2))
    order_fk = Column(Integer, ForeignKey("orders.id"))

    product = relationship("Product")
    order = relationship("Order", back_populates="items")
