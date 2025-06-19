from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class FitnessClassCreate(BaseModel):
    name: str
    dateTime: datetime = Field(..., alias="dateTime")
    instructor: str
    availableSlots: int = Field(..., alias="availableSlots")

class FitnessClassOut(BaseModel):
    id: int
    name: str
    dateTime: datetime = Field(..., alias="dateTime")
    instructor: str
    availableSlots: int = Field(..., alias="availableSlots")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class BookingCreate(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr

class BookingOut(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: EmailStr

    class Config:
        orm_mode = True 