from fastapi import UploadFile, HTTPException
from api.repository.property_repository import PropertyRepository
from schemas import schemas
from sqlalchemy.orm import Session

class PropertyService:
    def __init__(self, repository: PropertyRepository):
        self.repository = repository

    def create_property_type(self, property_type: schemas.PropertyTypeBase):
        return self.repository.create_property_type(property_type)

    def get_all_property_types(self):
        return self.repository.get_all_property_types()

    def get_property_type_by_id(self, property_type_id: int):
        return self.repository.get_property_type_by_id(property_type_id)
    
    def create_business_type(self, business_type: schemas.BusinessType):
        return self.repository.create_business_type(business_type)
    
    def get_all_business_types(self):
        return self.repository.get_all_business_type()
    
    def get_business_type_by_id(self, business_type_id: int):
        return self.repository.get_business_type_by_id(business_type_id)

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
    
    def get_properties_by_business_id(self, business_id: int):
        return self.repository.get_properties_by_business_id(business_id)
    
    def upload_and_save_image(self, property_id: int, image: UploadFile, is_cover: bool):
        return self.repository.upload_image_to_s3_and_save_url(property_id, image, is_cover)
    
    def get_properties_with_cover_images(self):
        properties = self.repository.get_properties_with_cover_images()
        return [
            schemas.PropertyWithCoverImage(
                title=property.title,
                description=property.description,
                price=property.price,
                property_type_id=property.property_type_id,
                facilities = property.facilities,
                city=property.city,
                zip_code=property.zip_code,
                address=property.address,
                latitude=property.latitude,
                longitude=property.longitude,
                business_type_id=property.business_type_id,
                cover_image_url=property.property_images[0].image_url  # Assuming the join gives us at least one image
            )
            for property in properties
        ]
    
    def get_property_details(self, property_id: int):
        property = self.repository.get_property_details(property_id)
        if property is None:
            raise HTTPException(status_code=404, detail="Property not found")
        # Fetch country name and business type name
        property_type_name = self.repository.get_property_type_name(property.property_type_id)
        country_name = self.repository.get_country_name(property.country_id)
        business_type_name = self.repository.get_business_type_name(property.business_type_id)

        return schemas.PropertyDetail(
                   title=property.title,
                   description=property.description,
                   price=property.price,
                   property_type_id=property.property_type_id,
                   facilities = property.facilities,
                   country_id=property.country_id,
                   city=property.city,
                   zip_code=property.zip_code,
                   address=property.address,
                   latitude=property.latitude,
                   longitude=property.longitude,
                   business_type_id=property.business_type_id,
                   created_at=property.created_at,  
                   updated_at=property.updated_at, 
                   created_by=property.created_by,
                   images=[
                       schemas.PropertyImageBase(
                           property_id=property_id,
                           image_url=image.image_url,
                           is_cover=image.is_cover
                       )
                       for image in property.property_images
                   ],
                   property_type_name=property_type_name,
                   country_name=country_name,
                   business_type_name=business_type_name
               )
           

    def create_subscription_type(self, subscription_type: schemas.SubscriptionType):
        return self.repository.create_subscription_type(subscription_type)
    
    def get_all_subscription_types(self):
        return self.repository.get_all_subscription_types()
    
    def create_subscription(self, subscription: schemas.SubscriptionCreate):
        return self.repository.create_subscription(subscription)
    
    def get_all_subscriptions(self):
        return self.repository.get_all_subscriptions()

    def get_property_with_subscription(self):
        properties_with_subscription = self.repository.get_property_with_subscription()
        result = []

        for property in properties_with_subscription:
            subscription_info = {
                'user_id': property.created_by,
                'property_id': property.id,
                'subscription_type_id': None,
                'start_date': None,
                'end_date': None,
                'cover_image_url': property.property_images[0].image_url
            }

            # Check if the property has a subscription
            if property.subscriptions:
                subscription_info.update({
                    'subscription_type_id': property.subscriptions[0].subscription_type_id,
                    'start_date': property.subscriptions[0].start_date,
                    'end_date': property.subscriptions[0].end_date
                })

            result.append(subscription_info)

        response_model = PropertyWithSubscriptionResponse(properties=result)
        return JSONResponse(content=response_model.dict())

    def get_property_with_subscription_by_subscription_type(self, subscription_type_id: int):
        return self.repository.get_property_with_subscription_by_subscription_type(subscription_type_id)