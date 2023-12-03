from typing import List
from fastapi import UploadFile
from sqlalchemy.orm import Session
from models import models
from schemas import schemas
from util.s3_util import upload_file_to_s3

class PropertyRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_property_type(self, property_type: schemas.PropertyTypeBase):
        db_property_type = models.PropertyType(type=property_type.type)
        self.db.add(db_property_type)
        self.db.commit()
        self.db.refresh(db_property_type)
        return db_property_type
    
    def create_business_type(self, business_type: schemas.BusinessType):
        db_business_type = models.BusinessType(type=business_type.type)
        self.db.add(db_business_type)
        self.db.commit()
        self.db.refresh(db_business_type)
        return db_business_type
    def get_all_business_type(self):
        return self.db.query(models.BusinessType).all()
    
    def get_business_type_by_id(self, business_type_id: int):
        return self.db.query(models.BusinessType).filter(models.BusinessType.id == business_type_id).first()

    def get_all_property_types(self):
        return self.db.query(models.PropertyType).all()

    def get_property_type_by_id(self, property_type_id: int):
        return self.db.query(models.PropertyType).filter(models.PropertyType.id == property_type_id).first()

    # Similarly add methods for 'Country' and 'Property'
    def create_country(self, country: schemas.CountryBase):
        db_country = models.Country(name=country.name)
        self.db.add(db_country)
        self.db.commit()
        self.db.refresh(db_country)
        return db_country
    
    def get_all_countries(self):
        return self.db.query(models.Country).all()
    
    def get_country_by_id(self, country_id: int):
        return self.db.query(models.Country).filter(models.Country.id == country_id).first()
    
    def create_property(self, property: schemas.PropertyBase):
        db_property = models.Property(**property.model_dump())
        self.db.add(db_property)
        self.db.commit()
        self.db.refresh(db_property)
        return db_property
    
    def get_all_properties(self):
       return self.db.query(models.Property).all()
    
    def get_property_by_type(self, type_id: int):
        return self.db.query(models.Property).filter(models.Property.property_type_id == type_id).all()
    
    def get_property_by_location(self, location: str):
        return self.db.query(models.Property).filter(models.Property.city == location).all()
    
    def get_property_by_user_id(self, user_id: int):
        return self.db.query(models.Property).filter(models.Property.created_by == user_id).all()
    
    def get_properties_by_business_id(self, business_id: int):
        return self.db.query(models.Property).filter(models.Property.business_type_id == business_id).all()
    
    async def upload_image_to_s3_and_save_url(self, property_id: int, image: UploadFile, is_cover: bool):
       # Upload the image to S3 and get the URL
       image_url = await upload_file_to_s3(image)
       
       # Create a new PropertyImage instance and add to the session
       db_property_image = models.PropertyImages(property_id=property_id, image_url=image_url, is_cover=is_cover)
       self.db.add(db_property_image)
       self.db.commit()
       self.db.refresh(db_property_image)
       
       return db_property_image
    
    def get_properties_with_cover_images(self):
        return (
            self.db.query(models.Property)
            .join(models.PropertyImages)  # This joins the Property with PropertyImages
            .filter(models.PropertyImages.is_cover == True)  # Filters for cover images
            .all()
        )
    
    def get_property_details(self, property_id: int):
        return (
            self.db.query(models.Property)
            .join(models.PropertyImages)
            .filter(models.Property.id == property_id)
            .first()
        )
        
    def get_country_name(self, property_id: int):
        country = (
            self.db.query(models.Country.name)
            .join(models.Property, models.Country.id == models.Property.country_id)
            .filter(models.Property.id == property_id)
            .first()
    )
        return country.name if country else None

    def get_business_type_name(self, property_id: int):
        business_type = (
            self.db.query(models.BusinessType.type)
            .join(models.Property, models.BusinessType.id == models.Property.business_type_id)
            .filter(models.Property.id == property_id)
            .first()
        )
        return business_type.type if business_type else None
    
    def get_property_type_name(self, property_id: int):
        property_type = (
            self.db.query(models.PropertyType.type)
            .join(models.Property, models.PropertyType.id == models.Property.property_type_id)
            .filter(models.Property.id == property_id)
            .first()
        )
        return property_type.type if property_type else None
    
    def create_subscription_type(self, subscription_type: schemas.SubscriptionType):
        db_subscription_type = models.SubscriptionType(**subscription_type.model_dump())
        self.db.add(db_subscription_type)
        self.db.commit()
        self.db.refresh(db_subscription_type)
        return db_subscription_type
    
    def get_all_subscription_types(self):
        return self.db.query(models.SubscriptionType).all()
    
    def create_subscription(self, subscription: schemas.SubscriptionCreate):
        db_subscription = models.Subscription(**subscription.model_dump())
        self.db.add(db_subscription)
        self.db.commit()
        self.db.refresh(db_subscription)
        return db_subscription
    
    def get_all_subscriptions(self):
        return self.db.query(models.Subscription).all()

    def get_property_with_subscription(self):
        return (
            self.db.query(models.Property)
            .join(models.Subscription)
            .filter(models.Property.id == models.Subscription.property_id)
            .all()
        )

    def get_property_with_subscription_by_subscription_type(self, subscription_type_id: int):
        return (
            self.db.query(models.Property)
            .join(models.Subscription)
            .filter(models.Subscription.subscription_type_id == subscription_type_id)
            .all()
        )


    
    