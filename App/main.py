from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import requests
from . import utils, models, pydantic_schemas
from .db import SessionLocal, engine, Base
import requests
from typing import Optional

app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_exchange_rate(currency: str):
    if currency == "PLN":
        return 1.0
    response = requests.get(f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/?format=json")
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Currency not supported")
    data = response.json()
    return data["rates"][0]["mid"]

@app.post("/orders/")
def create_order(order: pydantic_schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = utils.create_order(db=db, order=order)
    return db_order

@app.put("/orders/{order_id}/")
def update_order_status(order_id: int, order_update: pydantic_schemas.OrderUpdateStatus, db: Session = Depends(get_db)):

    order = utils.update_order_status(db=db, order_id=order_id, status=order_update.status)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return JSONResponse({},200)


@app.get("/orders/{order_id}/", response_model=pydantic_schemas.OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = utils.get_order(db=db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    exchange_rate = get_exchange_rate(order.currency)
    converted_amount = order.total_amount / exchange_rate
    return pydantic_schemas.OrderResponse(
        id=order.id,
        customer_name=order.customer_name,
        total_amount=order.total_amount,
        currency=order.currency,
        status=order.status,
        converted_amount=converted_amount
    )

@app.get("/orders/", response_model=list[pydantic_schemas.OrderResponse])
def list_orders(status: str = Query(None), db: Session = Depends(get_db)):
    orders = utils.get_orders(db=db, status=status)
    
    for order in orders:
        exchange_rate = get_exchange_rate(order.currency)
        converted_amount = order.total_amount / exchange_rate
        order.converted_amount = converted_amount
        
    return orders