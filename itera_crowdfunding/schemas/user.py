from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime

class UserBase(BaseModel):
    id: Optional[str] = None
    nik: Optional[str] = None
    prodi: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[Literal['admin','user']] = "user"
    photo_url: Optional[str] = None
    total_donation: Optional[int] = None
    created_at: Optional[datetime] = None

class UserCreate(UserBase):
    name: str
    email: str

class UserUpdate(UserBase):
    pass 
