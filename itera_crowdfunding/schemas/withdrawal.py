from pydantic import BaseModel
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime

class WithdrawalBase(BaseModel):
    campaign_id: Optional[int] = None
    amount: Optional[float] = None
    withdrawal_date: Optional[datetime] = None
    created_by: Optional[str] = None
    status: Optional[Literal['pending', 'approved', 'completed', 'rejected']] = 'pending'

class WithdrawalCreate(WithdrawalBase):
    campaign_id: int
    amount: float
    created_by: str

class WithdrawalUpdate(WithdrawalBase):
    pass
