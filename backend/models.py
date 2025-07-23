from pydantic import BaseModel
from typing import List, Literal

class OrderBookLevel(BaseModel):
    price: float
    amount: float

class OrderBookSnapshot(BaseModel):
    exchange: Literal["binance", "kraken", "bybit"]
    symbol: str
    bids: List[OrderBookLevel]
    asks: List[OrderBookLevel]
    timestamp: float
    