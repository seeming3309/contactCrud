from pydantic import BaseModel, Field
from typing import Optional

class Contact(BaseModel):
    id: int
    name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=3)

class ContactCreate(BaseModel):
    name: str
    phone: str

class ContactPatch(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
