from pydantic import BaseModel, Field
from typing import Optional, Literal
from uuid import UUID

class DonationBase(BaseModel):
    campaign: Optional[int] = None
    donor: Optional[str] = None
    amount: Optional[float] = None
    is_anonymous: Optional[bool] = False
    message: Optional[str] = None
    status: Optional[Literal['pending', 'paid', 'failed']] = 'pending'
    transaction: Optional[int] = None

class DonationCreate(DonationBase):
    campaign: int
    donor: str
    amount: float

class DonationUpdate(DonationBase):
    pass
