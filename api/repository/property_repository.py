from sqlalchemy.orm import Session
from models import models
from schemas import schemas

class PropertyRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_property_type(self, property_type: schemas.PropertyTypeBase):
        db_property_type = models.PropertyType(type=property_type.type)
        self.db.add(db_property_type)
        self.db.commit()
        self.db.refresh(db_property_type)
        return db_property_type

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
    