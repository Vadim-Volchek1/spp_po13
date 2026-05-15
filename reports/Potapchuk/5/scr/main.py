from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db

app = FastAPI(title="Rental Service", version="0.1.0")


@app.post("/offers/", status_code=201)
def create_offer(
    title: str,
    description: str,
    user_id: int,
    category_id: int,
    db: Session = Depends(get_db),
) -> dict:
    """Create new offer"""
    offer = models.Offer(
        title=title,
        description=description,
        user_id=user_id,
        category_id=category_id,
    )
    db.add(offer)
    db.commit()
    db.refresh(offer)
    return {"status": "created", "id": offer.id}


@app.get("/offers/")
def get_offers(db: Session = Depends(get_db)) -> List[models.Offer]:
    """Get all offers"""
    return db.query(models.Offer).all()


@app.delete("/offers/{offer_id}")
def delete_offer(offer_id: int, db: Session = Depends(get_db)) -> dict:
    """Delete offer"""
    offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if offer is None:
        raise HTTPException(status_code=404, detail="Offer not found")

    db.delete(offer)
    db.commit()
    return {"status": "deleted"}


@app.post("/demands/", status_code=201)
def create_demand(
    title: str,
    description: str,
    user_id: int,
    category_id: int,
    db: Session = Depends(get_db),
) -> dict:
    """Create demand"""
    demand = models.Demand(
        title=title,
        description=description,
        user_id=user_id,
        category_id=category_id,
    )
    db.add(demand)
    db.commit()
    db.refresh(demand)
    return {"status": "created", "id": demand.id}


@app.get("/demands/")
def get_demands(db: Session = Depends(get_db)) -> List[models.Demand]:
    """Get all demands"""
    return db.query(models.Demand).all()


@app.post("/exchange/", status_code=201)
def create_exchange(
    offer_id: int, demand_id: int, db: Session = Depends(get_db)
) -> dict:
    """Create exchange"""
    exchange = models.Exchange(
        offer_id=offer_id,
        demand_id=demand_id,
        status="pending",
    )
    db.add(exchange)
    db.commit()
    db.refresh(exchange)
    return {"status": "created", "id": exchange.id}


@app.get("/exchange/")
def get_exchanges(db: Session = Depends(get_db)) -> List[models.Exchange]:
    """Get all exchanges"""
    return db.query(models.Exchange).all()


@app.post("/reviews/", status_code=201)
def create_review(
    author_id: int,
    target_id: int,
    rating: int,
    comment: str,
    db: Session = Depends(get_db),
) -> dict:
    """Create review"""
    review = models.Review(
        author_id=author_id,
        target_id=target_id,
        rating=rating,
        comment=comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return {"status": "created", "id": review.id}
