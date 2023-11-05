from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, ARRAY, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from config.database import Base
from datetime import datetime
import enum

class BusinessType(Base):
    __tablename__ = 'business_types'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, unique=True)

    # Relationship - BusinessType can be associated with many properties
    properties = relationship("Property", back_populates="business_type")
 
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    hashed_password = Column(String)

    # Relationship - User can have many properties
    properties = relationship("Property", back_populates="creator")

class PropertyType(Base):
    __tablename__ = 'property_types'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, unique=True)

    # Relationship - PropertyType can be associated with many properties
    properties = relationship("Property", back_populates="property_type")

class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    # Relationship - A Country can have many properties
    properties = relationship("Property", back_populates="country")

class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    property_type_id = Column(Integer, ForeignKey('property_types.id'))
   # images = Column(ARRAY(String), nullable=True)  # PostgreSQL ARRAY
    facilities = Column(JSONB)  # PostgreSQL JSONB
    country_id = Column(Integer, ForeignKey('countries.id'))
    city = Column(String)
    zip_code = Column(String)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    business_type_id = Column(Integer, ForeignKey('business_types.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))
    is_active = Column(Boolean, default=True)

      # Relationships
    property_type = relationship("PropertyType", back_populates="properties")
    country = relationship("Country", back_populates="properties")
    creator = relationship("User", back_populates="properties")
    business_type = relationship("BusinessType", back_populates="properties")
    property_images = relationship("PropertyImages", back_populates="property")


class PropertyImages(Base):
    __tablename__ = 'property_images'
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey('properties.id'))
    image_url = Column(String)
    is_cover = Column(Boolean, default= False)


    property = relationship("Property", back_populates="property_images")

  

