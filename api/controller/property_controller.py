from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from starlette import status
from sqlalchemy.orm import Session
from config.database import get_db
from schemas import schemas
from models import models
from api.service.property_service import PropertyService
from api.repository.property_repository import PropertyRepository
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import os

load_dotenv()


router = APIRouter(
    prefix='/api/v1/property',
    tags=['property']
)


db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/property_types", status_code=status.HTTP_201_CREATED)
async def create_property_type(property_type: schemas.PropertyTypeBase, db: db_dependency):
    service = PropertyService(PropertyRepository(db))
    return service.create_property_type(property_type)

@router.get("/property_types/", response_model=list[schemas.PropertyTypeBase])
async def get_all_property_types(db: db_dependency):
    service = PropertyService(PropertyRepository(db))
    return service.get_all_property_types()

@router.get("/property_types/{property_type_id}", response_model=schemas.PropertyTypeBase)
async def get_property_type_by_id(db: db_dependency, property_type_id: int):
    service = PropertyService(PropertyRepository(db))
    property_type = service.get_property_type_by_id(property_type_id)
    if property_type is None:
        raise HTTPException(status_code=404, detail="PropertyType not found")
    return property_type

@router.post("/countries", status_code=status.HTTP_201_CREATED)
async def create_country(country: schemas.CountryBase, db: db_dependency):
    service = PropertyService(PropertyRepository(db))
    return service.create_country(country)

@router.get("/countries/", response_model=list[schemas.CountryBase])
async def get_all_countries(db: db_dependency):
    service = PropertyService(PropertyRepository(db))
    return service.get_all_countries()

@router.get("/countries/{country_id}", response_model=schemas.CountryBase)
async def get_country_by_id(db: db_dependency, country_id: int):
    service = PropertyService(PropertyRepository(db))
    country = service.get_country_by_id(country_id)
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

@router.post("/business_types", status_code=status.HTTP_201_CREATED)
async def create_business_type(business_type: schemas.BusinessType, db: db_dependency):
    service = PropertyService(PropertyRepository(db))
    return service.create_business_type(business_type)

@router.get("/business_types/", response_model=list[schemas.BusinessType])
async def get_all_business_types(db: db_dependency):
    service = PropertyService(PropertyRepository(db))
    return service.get_all_business_types()

@router.get('/business_types/{business_type_id}', response_model=schemas.BusinessType)
async def get_business_type_by_id(db: db_dependency, business_type_id: int):
    service = PropertyService(PropertyRepository(db))
    business_type = service.get_business_type_by_id(business_type_id)
    if business_type is None:
        raise HTTPException(status_code=404, detail="BusinessType not found")
    return business_type

@router.post("/properties", status_code=status.HTTP_201_CREATED)
async def create_property(property: schemas.PropertyBase, db: db_dependency):
    service = PropertyService(PropertyRepository(db))
    return service.create_property(property)

@router.get("/properties/", response_model=list[schemas.PropertyBase])
async def get_all_properties(db: db_dependency):
    service = PropertyService(PropertyRepository(db))
    return service.get_all_properties()

@router.get("/type/{type_id}", response_model=list[schemas.PropertyBase])
async def get_properties_by_property_type_id(db: db_dependency, type_id: int):
    service = PropertyService(PropertyRepository(db))
    properties = service.get_property_by_type(type_id)
    if properties is None:
        raise HTTPException(status_code=404, detail="Properties not found")
    return service.get_property_by_type(type_id)

@router.get("/location/{location}", response_model=list[schemas.PropertyBase])
async def get_properties_by_location(db: db_dependency, location: str):
    service = PropertyService(PropertyRepository(db))
    properties = service.get_property_by_location(location)
    if properties is None:
        raise HTTPException(status_code=404, detail="Properties not found")
    return service.get_property_by_location(location)

@router.get("/user/{user_id}", response_model=list[schemas.PropertyBase])
async def get_properties_by_user_id(db: db_dependency, user_id: int):
    service = PropertyService(PropertyRepository(db))
    properties = service.get_property_by_user_id(user_id)
    if properties is None:
        raise HTTPException(status_code=404, detail="Properties not found")
    return service.get_property_by_user_id(user_id)

@router.get("/properties/with-cover-images", response_model=List[schemas.PropertyWithCoverImage])
async def get_properties_with_cover_images(db: db_dependency):
    service = PropertyService(PropertyRepository(db))
    properties_with_images = service.get_properties_with_cover_images()
    return properties_with_images

@router.get('/properties/{property_id}', response_model=schemas.PropertyDetail)
async def get_property_details(db: db_dependency, property_id: int):
    service = PropertyService(PropertyRepository(db))
    property = service.get_property_details(property_id)
    if property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return property

@router.get("/properties/{business_id}", response_model=list[schemas.PropertyBase])
async def get_properties_by_business_id(db: db_dependency, business_id: int):
    service = PropertyService(PropertyRepository(db))
    properties = service.get_properties_by_business_id(business_id)
    if properties is None:
        raise HTTPException(status_code=404, detail="Properties not found")
    return service.get_properties_by_business_id(business_id)

@router.post("/{property_id}/image/", response_model=schemas.PropertyImageBase)
async def upload_property_image(
    property_id: int,
    image: UploadFile = File(...),
    is_cover: bool = False,
    db: Session = Depends(get_db)
):
    service = PropertyService(PropertyRepository(db))
    try:
        property_image = await service.upload_and_save_image(property_id, image, is_cover)
    except NoCredentialsError as e:
        raise HTTPException(status_code=500, detail="AWS credentials not valid")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    return property_image

