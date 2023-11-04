from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List



class UserBase(BaseModel):
    name: str
    username: str
    email: str
    phone: str

class CreateUserRequest(UserBase):
    name: str
    username: str
    email: str
    password: str
    phone: str


class UserInDB(UserBase):
    id: int
    hashed_password: str
    created_at: datetime


class UserPublic(UserBase):
    id: int
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str

class PropertyTypeBase(BaseModel):
    type : str

class CountryBase(BaseModel):
    name: str

class PropertyBase(BaseModel):
    title: str
    description: str
    price: float
    property_type_id: int
    images: List[str]  # Updated field
    facilities: dict
    country_id: int
    city: str
    zip_code: str
    address: str
    latitude: float
    longitude: float
    created_at: datetime 
    updated_at: datetime  
    created_by: int
    is_active: bool = True

    class Config:
        orm_mode = True

class PropertyRead(PropertyBase):
    id: int  # Assuming an ID field for identification

    class Config:
        orm_mode = True