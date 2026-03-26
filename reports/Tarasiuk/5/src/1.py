from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from datetime import datetime

DATABASE_URL = "postgresql"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    offers = relationship("Offer", back_populates="user")
    demands = relationship("Demand", back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="offers")


class Demand(Base):
    __tablename__ = "demands"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="demands")


class Exchange(Base):
    __tablename__ = "exchanges"

    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    demand_id = Column(Integer, ForeignKey("demands.id"))
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    target_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer)
    comment = Column(Text)


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(username: str, email: str, db: Session = Depends(get_db)):
    user = User(username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.put("/users/{user_id}")
def update_user(user_id: int, username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = username
    db.commit()
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"status": "deleted"}

@app.post("/offers/")
def create_offer(title: str, description: str, user_id: int, category_id: int, db: Session = Depends(get_db)):
    offer = Offer(title=title, description=description, user_id=user_id, category_id=category_id)
    db.add(offer)
    db.commit()
    db.refresh(offer)
    return offer


@app.get("/offers/")
def get_offers(db: Session = Depends(get_db)):
    return db.query(Offer).all()


@app.delete("/offers/{offer_id}")
def delete_offer(offer_id: int, db: Session = Depends(get_db)):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    db.delete(offer)
    db.commit()
    return {"status": "deleted"}

@app.post("/demands/")
def create_demand(title: str, description: str, user_id: int, category_id: int, db: Session = Depends(get_db)):
    demand = Demand(title=title, description=description, user_id=user_id, category_id=category_id)
    db.add(demand)
    db.commit()
    db.refresh(demand)
    return demand


@app.get("/demands/")
def get_demands(db: Session = Depends(get_db)):
    return db.query(Demand).all()

@app.post("/exchange/")
def create_exchange(offer_id: int, demand_id: int, db: Session = Depends(get_db)):
    exchange = Exchange(offer_id=offer_id, demand_id=demand_id, status="pending")
    db.add(exchange)
    db.commit()
    db.refresh(exchange)
    return exchange


@app.get("/exchange/")
def get_exchanges(db: Session = Depends(get_db)):
    return db.query(Exchange).all()

@app.post("/reviews/")
def create_review(author_id: int, target_id: int, rating: int, comment: str, db: Session = Depends(get_db)):
    review = Review(author_id=author_id, target_id=target_id, rating=rating, comment=comment)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@app.get("/reviews/")
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()
