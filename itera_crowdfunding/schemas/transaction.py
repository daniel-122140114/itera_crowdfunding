from pydantic import BaseModel
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime

class TransactionBase(BaseModel):
    order_id: Optional[str]
    donor_id: Optional[str]
    campaign_id: Optional[int]
    amount: Optional[float]
    payment_type: Optional[Literal['bank_transfer', 'gopay', 'shopeepay', 'qris', 'credit_card', 'indomaret', 'alfamart']]
    transaction_status: Optional[Literal['pending', 'settlement', 'cancel', 'expire']]
    transaction_time: Optional[datetime]
    settlement_time: Optional[datetime]
    va_numbers: Optional[str]
    fraud_status: Optional[str]

class TransactionCreate(TransactionBase):
    order_id: str
    donor_id: str
    campaign_id: int
    amount: float
    payment_type: str

class TransactionUpdate(TransactionBase):
    pass
