from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal

class CampaignBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type_id: Optional[int] = None
    image_url: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = 0
    status: Optional[Literal['pending', 'approved', 'completed', 'rejected']] = 'pending'
    is_urgent: Optional[Literal['normal', 'mendesak']] = 'normal'
    created_by: Optional[str] = None

class CampaignCreate(CampaignBase):
    title: str
    type_id: int
    target_amount: float
    created_by: str


class CampaignUpdate(CampaignBase):
    pass  # Semua opsional untuk update
