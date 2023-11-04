from api.repository.property_repository import PropertyRepository
from schemas import schemas

class PropertyService:
    def __init__(self, repository: PropertyRepository):
        self.repository = repository

    def create_property_type(self, property_type: schemas.PropertyTypeBase):
        return self.repository.create_property_type(property_type)

    def get_all_property_types(self):
        return self.repository.get_all_property_types()

    def get_property_type_by_id(self, property_type_id: int):
        return self.repository.get_property_type_by_id(property_type_id)

    def create_country(self, country: schemas.CountryBase):
        return self.repository.create_country(country)
    
    def get_all_countries(self):
        return self.repository.get_all_countries()
    
    def get_country_by_id(self, country_id: int):
        return self.repository.get_country_by_id(country_id)
    
    def create_property(self, property: schemas.PropertyBase):
        return self.repository.create_property(property)
    
    def get_all_properties(self):
        return self.repository.get_all_properties()
    
    def get_property_by_type(self, type_id: int):
        return self.repository.get_property_by_type(type_id)
    
    def get_property_by_location(self, location: str):
        return self.repository.get_property_by_location(location)
    
    def get_property_by_user_id(self, user_id: int):
        return self.repository.get_property_by_user_id(user_id)
