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

    

    
    