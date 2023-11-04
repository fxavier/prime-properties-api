from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from config.database import get_db
from schemas import schemas
from models import models
from api.service.property_service import PropertyService
from api.repository.property_repository import PropertyRepository

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