from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# Модель для пользователя
class Customer(Base):
    __tablename__ = "Customer"

    id = Column(Integer, primary_key=True, index=True)
    fnane = Column(String(100))
    sname = Column(String(100))
    adres = Column(Text)
    phone = Column(String(20))

    # Связь с заказами
    orders = relationship("Order", back_populates="customer")


# Модель для заказа
class Order(Base):
    __tablename__ = "Orders"

    id = Column(Integer, primary_key=True, index=True)
    id_customer = Column(Integer, ForeignKey("Customer.id", ondelete="CASCADE"))
    date = Column(DateTime, default=datetime.now)

    # Связи
    customer = relationship("Customer", back_populates="orders")
    items = relationship("NaborOrder", back_populates="order")


# Модель для склада
class Sclad(Base):
    __tablename__ = "Sclad"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    adres = Column(Text)

    # Связь с товарами
    goods = relationship("Good", back_populates="sclad")


# Модель для товаров
class Good(Base):
    __tablename__ = "Goods"

    id = Column(Integer, primary_key=True, index=True)
    id_sclad = Column(Integer, ForeignKey("Sclad.id", ondelete="SET NULL"))
    name = Column(String(255))
    postavshchik = Column(String(255))
    stoimost = Column(Numeric(10, 2))

    # Связи
    sclad = relationship("Sclad", back_populates="goods")
    order_items = relationship("NaborOrder", back_populates="good")


# Модель для наборов заказов
class NaborOrder(Base):
    __tablename__ = "NaborOrders"

    id_order = Column(
        Integer, ForeignKey("Orders.id", ondelete="CASCADE"), primary_key=True
    )
    id_good = Column(
        Integer, ForeignKey("Goods.id", ondelete="CASCADE"), primary_key=True
    )
    count = Column(Integer, nullable=False)

    # Связи
    order = relationship("Order", back_populates="items")
    good = relationship("Good", back_populates="order_items")
