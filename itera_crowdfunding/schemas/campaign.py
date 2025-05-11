from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal

class CampaignBase(BaseModel):
    title: Optional[str]
    description: Optional[str]
    type_id: Optional[int]
    image_url: Optional[str]
    target_amount: Optional[float]
    current_amount: Optional[float] = 0
    status: Optional[Literal['pending', 'approved', 'completed', 'rejected']] = 'pending'
    is_urgent: Optional[Literal['normal', 'mendesak']] = 'normal'
    created_by: Optional[str]

class CampaignCreate(CampaignBase):
    title: str
    type_id: int
    target_amount: float
    created_by: str


class CampaignUpdate(CampaignBase):
    pass  # Semua opsional untuk update
