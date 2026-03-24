from sqlalchemy.orm import Session
import crud
import schemas
from database import get_db
from typing import List
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI(title="Company API")


# Эндпоинты пользователя
@app.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)


@app.get("/customers/", response_model=List[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers


@app.get("/customers/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


@app.put("/customers/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = crud.update_customer(db, customer_id, customer)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.delete_customer(db, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}


# Эндпоинты заказа
@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)


@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip=skip, limit=limit)


@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.delete_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}


# Эндпоинты заказа
@app.post("/goods/", response_model=schemas.Good)
def create_good(good: schemas.GoodCreate, db: Session = Depends(get_db)):
    return crud.create_good(db, good)


@app.get("/goods/", response_model=List[schemas.Good])
def read_goods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_goods(db, skip=skip, limit=limit)


@app.get("/goods/{good_id}", response_model=schemas.Good)
def read_good(good_id: int, db: Session = Depends(get_db)):
    db_good = crud.get_good(db, good_id)
    if db_good is None:
        raise HTTPException(status_code=404, detail="Good not found")
    return db_good


@app.put("/goods/{good_id}", response_model=schemas.Good)
def update_good(good_id: int, good: schemas.GoodCreate, db: Session = Depends(get_db)):
    db_good = crud.update_good(db, good_id, good)
    if db_good is None:
        raise HTTPException(status_code=404, detail="Good not found")
    return db_good


@app.delete("/goods/{good_id}")
def delete_good(good_id: int, db: Session = Depends(get_db)):
    db_good = crud.delete_good(db, good_id)
    if db_good is None:
        raise HTTPException(status_code=404, detail="Good not found")
    return {"message": "Good deleted successfully"}


# Эндпоинты состава заказа
@app.get("/orders/{order_id}/items", response_model=List[schemas.NaborOrder])
def read_order_items(order_id: int, db: Session = Depends(get_db)):
    return crud.get_nabor_orders_by_order(db, order_id)


@app.post("/orders/{order_id}/items", response_model=schemas.NaborOrder)
def add_item_to_order(order_id: int, item: schemas.NaborOrderCreate, db: Session = Depends(get_db)):
    # Проверяем, что order_id в пути совпадает с item.id_order
    if item.id_order != order_id:
        raise HTTPException(status_code=400, detail="Order ID mismatch")
    return crud.add_item_to_order(db, item)


@app.delete("/orders/{order_id}/items/{good_id}")
def remove_item_from_order(order_id: int, good_id: int, db: Session = Depends(get_db)):
    result = crud.remove_item_from_order(db, order_id, good_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found in order")
    return {"message": "Item removed from order"}


# Эндпоинт склада
@app.post("/sclads/", response_model=schemas.Sclad)
def create_sclad(sclad: schemas.ScladCreate, db: Session = Depends(get_db)):
    return crud.create_sclad(db, sclad)


@app.get("/sclads/", response_model=List[schemas.Sclad])
def read_sclads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_sclads(db, skip=skip, limit=limit)


@app.get("/sclads/{sclad_id}", response_model=schemas.Sclad)
def read_sclad(sclad_id: int, db: Session = Depends(get_db)):
    db_sclad = crud.get_sclad(db, sclad_id)
    if db_sclad is None:
        raise HTTPException(status_code=404, detail="Sclad not found")
    return db_sclad


@app.delete("/sclads/{sclad_id}")
def delete_sclad(sclad_id: int, db: Session = Depends(get_db)):
    db_sclad = crud.delete_sclad(db, sclad_id)
    if db_sclad is None:
        raise HTTPException(status_code=404, detail="Sclad not found")
    return {"message": "Sclad deleted successfully"}