from pydantic import BaseModel
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime

class TransactionBase(BaseModel):
    order_id: Optional[str] = None
    donor_id: Optional[str] = None
    campaign_id: Optional[int] = None
    amount: Optional[float] = None
    payment_type: Optional[Literal['bank_transfer', 'gopay', 'shopeepay', 'qris', 'credit_card', 'indomaret', 'alfamart']]
    transaction_status: Optional[Literal['pending', 'settlement', 'cancel', 'expire']]
    transaction_time: Optional[datetime] = None
    settlement_time: Optional[datetime] = None
    va_numbers: Optional[str] = None
    fraud_status: Optional[str] = None

class TransactionCreate(TransactionBase):
    order_id: str
    donor_id: str
    campaign_id: int
    amount: float
    payment_type: str

class TransactionUpdate(TransactionBase):
    pass
