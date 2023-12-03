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
    is_subscribed = Column(Boolean, default=False)
    subscription_expiry_date = Column(DateTime, nullable=True)

    # Relationship - User can have many properties
    properties = relationship("Property", back_populates="creator")
    subscriptions = relationship("Subscription", back_populates="user")

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
    is_featured = Column(Boolean, default=False)
    is_prioritized = Column(Boolean, default=False)
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
    subscriptions = relationship("Subscription", back_populates="property")


class PropertyImages(Base):
    __tablename__ = 'property_images'
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey('properties.id'))
    image_url = Column(String)
    is_cover = Column(Boolean, default= False)


    property = relationship("Property", back_populates="property_images")

class SubscriptionType(Base):
    __tablename__ = 'subscription_types'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, unique=True)
    price = Column(Float)
    duration = Column(Integer)
    is_active = Column(Boolean, default=True)

class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    property_id = Column(Integer, ForeignKey('properties.id'))
    subscription_type_id = Column(Integer, ForeignKey('subscription_types.id'))
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="subscriptions")
    property = relationship("Property", back_populates="subscriptions")
    subscription_type = relationship("SubscriptionType")

  

