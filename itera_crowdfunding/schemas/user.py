from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime

class UserBase(BaseModel):
    id: Optional[str]
    nik: Optional[str]
    prodi: Optional[str]
    name: Optional[str]
    email: Optional[str]
    role: Optional[Literal['admin','user']]
    photo_url: Optional[str]
    total_donation: Optional[int]
    created_at: Optional[datetime]

class UserCreate(UserBase):
    name: str
    email: str
    prodi: Optional[str]
    nik: Optional[str]

class UserUpdate(UserBase):
    pass 
