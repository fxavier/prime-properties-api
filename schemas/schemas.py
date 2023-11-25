from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class BusinessType(BaseModel):
    type: str
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
   # images: List[str] = [] # Updated field
    facilities: dict
    country_id: int
    city: str
    zip_code: str
    address: str
    latitude: float
    longitude: float
    business_type_id: int
    created_at: datetime 
    updated_at: datetime  
    created_by: int
    is_active: bool = True

    class Config:
        orm_mode = True

class PropertyImageBase(BaseModel):
    property_id: int
    image_url: str
    is_cover: bool = False

    class Config:
        orm_mode = True

class PropertyRead(PropertyBase):
    id: int  # Assuming an ID field for identification

    class Config:
        orm_mode = True

class PropertyWithCoverImage(BaseModel):
    # Include all fields from the Property model that you want to expose
    title: str
    description: str
    price: float
    property_type_id: int
    facilities: dict
    city: str
    zip_code: str
    address: str
    latitude: float
    longitude: float
    business_type_id: int
    cover_image_url: str  # This will hold the URL of the cover image

    class Config:
        orm_mode = True

class PropertyDetail(PropertyBase):
    images: List[PropertyImageBase]
    property_type_name: Optional[str] = None
    country_name: Optional[str] = None  
    business_type_name: Optional[str] = None

    class Config:
        orm_mode = True