from pydantic import BaseModel, Field
from typing import Optional, Literal
from uuid import UUID

class DonationBase(BaseModel):
    campaign_id: Optional[int]
    donor_id: Optional[str]
    amount: Optional[float]
    is_anonymous: Optional[bool] = False
    message: Optional[str]
    status: Optional[Literal['pending', 'paid', 'failed']] = 'pending'
    payment_id: Optional[str]

class DonationCreate(DonationBase):
    campaign_id: int
    donor_id: str
    amount: float

class DonationUpdate(DonationBase):
    pass
