from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from config.database import get_db
from schemas import schemas
from models import models

router = APIRouter(
    prefix='/api/v1/property',
    tags=['property']
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/api/v1/property_types", status_code=status.HTTP_201_CREATED)
async def create_property_type(property_type: schemas.PropertyTypeBase, db: db_dependency):
    db_property_type = models.PropertyType(type=property_type.type)
    db.add(db_property_type)
    db.commit()
    db.refresh(db_property_type)
    return db_property_type

@router.get("/api/v1/property_types/", response_model=list[schemas.PropertyTypeBase])
async def read_all_property_types(db: db_dependency):
    db_property_types = db.query(models.PropertyType).all()
    return db_property_types

@router.get("/api/v1/property_types/{property_type_id}", response_model=schemas.PropertyTypeBase)
async def read_property_type(property_type_id: int, db: db_dependency):
    db_property_type = db.query(models.PropertyType).filter(models.PropertyType.id == property_type_id).first()
    if db_property_type is None:
        raise HTTPException(status_code=404, detail="PropertyType not found")
    return db_property_type

@router.post("/api/v1/countries/", status_code=status.HTTP_201_CREATED)
async def create_country(country: schemas.CountryBase, db: db_dependency):
    db_country = models.Country(name=country.name)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

@router.get("/countries/", response_model=list[schemas.CountryBase])
async def read_all_countries(db: db_dependency):
    db_countries = db.query(models.Country).all()
    return db_countries


@router.get("/countries/{country_id}", response_model=schemas.CountryBase)
async def read_country(country_id: int, db: db_dependency):
    db_country = db.query(models.Country).filter(models.Country.id == country_id).first()
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country

@router.post("/properties/", response_model=schemas.PropertyRead)
async def create_property(property: schemas.PropertyBase, db: db_dependency):
    db_property = models.Property(**property.model_dump())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

@router.get("/properties/", response_model=list[schemas.PropertyRead])
async def read_all_properties(db: Session = Depends(get_db)):
    db_properties = db.query(models.Property).all()
    return db_properties
