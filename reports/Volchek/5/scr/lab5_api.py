from datetime import date

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Date, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

engine = create_engine("sqlite:///./trade_activity.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Postavshik(Base):
    __tablename__ = "postavshiki"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(40))


class Tovar(Base):
    __tablename__ = "tovary"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer, default=0)


class Klient(Base):
    __tablename__ = "klienty"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(40))


class Zakupka(Base):
    __tablename__ = "zakupki"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    postavshik_id: Mapped[int] = mapped_column(ForeignKey("postavshiki.id"))
    tovar_id: Mapped[int] = mapped_column(ForeignKey("tovary.id"))
    qty: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[date] = mapped_column(Date)


class Prodazha(Base):
    __tablename__ = "prodazhi"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    klient_id: Mapped[int] = mapped_column(ForeignKey("klienty.id"))
    tovar_id: Mapped[int] = mapped_column(ForeignKey("tovary.id"))
    qty: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[date] = mapped_column(Date)


class PostavshikIn(BaseModel):
    name: str
    phone: str


class TovarIn(BaseModel):
    name: str
    price: float
    stock: int


class KlientIn(BaseModel):
    name: str
    phone: str


class ZakupkaIn(BaseModel):
    postavshik_id: int
    tovar_id: int
    qty: int
    created_at: date


class ProdazhaIn(BaseModel):
    klient_id: int
    tovar_id: int
    qty: int
    created_at: date


app = FastAPI(
    title="ЛР5: торгово-закупочная деятельность",
    version="1.0",
    openapi_version="3.0.3",
    swagger_ui_parameters={"layout": "BaseLayout"},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Сервер работает", "docs": "/docs"}


@app.get("/postavshiki")
def postavshiki_list(db: Session = Depends(get_db)):
    data = db.query(Postavshik).all()
    return [{"id": x.id, "name": x.name, "phone": x.phone} for x in data]


@app.post("/postavshiki")
def postavshiki_add(item: PostavshikIn, db: Session = Depends(get_db)):
    row = Postavshik(name=item.name, phone=item.phone)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "name": row.name, "phone": row.phone}


@app.get("/tovary")
def tovary_list(db: Session = Depends(get_db)):
    data = db.query(Tovar).all()
    return [{"id": x.id, "name": x.name, "price": x.price, "stock": x.stock} for x in data]


@app.post("/tovary")
def tovary_add(item: TovarIn, db: Session = Depends(get_db)):
    row = Tovar(name=item.name, price=item.price, stock=item.stock)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "name": row.name, "price": row.price, "stock": row.stock}


@app.put("/tovary/{tovar_id}")
def tovary_update(tovar_id: int, item: TovarIn, db: Session = Depends(get_db)):
    row = db.get(Tovar, tovar_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    row.name = item.name
    row.price = item.price
    row.stock = item.stock
    db.commit()
    return {"ok": True}


@app.delete("/tovary/{tovar_id}")
def tovary_delete(tovar_id: int, db: Session = Depends(get_db)):
    row = db.get(Tovar, tovar_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    db.delete(row)
    db.commit()
    return {"ok": True}


@app.get("/klienty")
def klienty_list(db: Session = Depends(get_db)):
    data = db.query(Klient).all()
    return [{"id": x.id, "name": x.name, "phone": x.phone} for x in data]


@app.post("/klienty")
def klienty_add(item: KlientIn, db: Session = Depends(get_db)):
    row = Klient(name=item.name, phone=item.phone)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "name": row.name, "phone": row.phone}


@app.get("/zakupki")
def zakupki_list(db: Session = Depends(get_db)):
    data = db.query(Zakupka).all()
    return [
        {
            "id": x.id,
            "postavshik_id": x.postavshik_id,
            "tovar_id": x.tovar_id,
            "qty": x.qty,
            "created_at": x.created_at,
        }
        for x in data
    ]


@app.post("/zakupki")
def zakupki_add(item: ZakupkaIn, db: Session = Depends(get_db)):
    post = db.get(Postavshik, item.postavshik_id)
    tovar = db.get(Tovar, item.tovar_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Поставщик не найден")
    if tovar is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    row = Zakupka(
        postavshik_id=item.postavshik_id,
        tovar_id=item.tovar_id,
        qty=item.qty,
        created_at=item.created_at,
    )
    tovar.stock = tovar.stock + item.qty
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "qty": row.qty}


@app.get("/prodazhi")
def prodazhi_list(db: Session = Depends(get_db)):
    data = db.query(Prodazha).all()
    return [
        {"id": x.id, "klient_id": x.klient_id, "tovar_id": x.tovar_id, "qty": x.qty, "created_at": x.created_at}
        for x in data
    ]


@app.post("/prodazhi")
def prodazhi_add(item: ProdazhaIn, db: Session = Depends(get_db)):
    kl = db.get(Klient, item.klient_id)
    tovar = db.get(Tovar, item.tovar_id)
    if kl is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    if tovar is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    if tovar.stock < item.qty:
        raise HTTPException(status_code=400, detail="На складе мало товара")
    row = Prodazha(klient_id=item.klient_id, tovar_id=item.tovar_id, qty=item.qty, created_at=item.created_at)
    tovar.stock = tovar.stock - item.qty
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "qty": row.qty}
