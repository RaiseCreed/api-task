from sqlalchemy.orm import Session
from . import models, pydantic_schemas
from typing import Optional
from fastapi.responses import JSONResponse

def create_order(db: Session, order: pydantic_schemas.OrderCreate):
    db_order = models.Order(
        customer_name=order.customer_name,
        total_amount=order.total_amount,
        currency=order.currency
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return JSONResponse({},201)

def update_order_status(db: Session, order_id: int, status: str):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order:
        
        order.status = status
        db.commit()
    return order

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, status: Optional[str] = None):
    query = db.query(models.Order)
    if status:
        query = query.filter(models.Order.status == status)
    return query.all()