from sqlalchemy.orm import Session
import models
import schemas


# ПОЛЬЗОВАТЕЛЬ
def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def update_customer(db: Session, customer_id: int, customer: schemas.CustomerCreate):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        for key, value in customer.model_dump().items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer


# ЗАКАЗ
def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()


def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order


# ТОВАР
def get_good(db: Session, good_id: int):
    return db.query(models.Good).filter(models.Good.id == good_id).first()


def get_goods(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Good).offset(skip).limit(limit).all()


def create_good(db: Session, good: schemas.GoodCreate):
    db_good = models.Good(**good.model_dump())
    db.add(db_good)
    db.commit()
    db.refresh(db_good)
    return db_good


def update_good(db: Session, good_id: int, good: schemas.GoodCreate):
    db_good = get_good(db, good_id)
    if db_good:
        for key, value in good.model_dump().items():
            setattr(db_good, key, value)
        db.commit()
        db.refresh(db_good)
    return db_good


def delete_good(db: Session, good_id: int):
    db_good = get_good(db, good_id)
    if db_good:
        db.delete(db_good)
        db.commit()
    return db_good


# НАБОР ЗАКАЗА
def get_nabor_orders_by_order(db: Session, order_id: int):
    return (
        db.query(models.NaborOrder).filter(models.NaborOrder.id_order == order_id).all()
    )


def add_item_to_order(db: Session, item: schemas.NaborOrderCreate):
    db_item = models.NaborOrder(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def remove_item_from_order(db: Session, order_id: int, good_id: int):
    db_item = (
        db.query(models.NaborOrder)
        .filter(
            models.NaborOrder.id_order == order_id, models.NaborOrder.id_good == good_id
        )
        .first()
    )
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item


# СКЛАД
def get_sclad(db: Session, sclad_id: int):
    return db.query(models.Sclad).filter(models.Sclad.id == sclad_id).first()


def get_sclads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sclad).offset(skip).limit(limit).all()


def create_sclad(db: Session, sclad: schemas.ScladCreate):
    db_sclad = models.Sclad(**sclad.model_dump())
    db.add(db_sclad)
    db.commit()
    db.refresh(db_sclad)
    return db_sclad


def delete_sclad(db: Session, sclad_id: int):
    db_sclad = get_sclad(db, sclad_id)
    if db_sclad:
        db.delete(db_sclad)
        db.commit()
    return db_sclad
