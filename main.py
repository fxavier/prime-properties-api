from fastapi import FastAPI
from api.auth import auth
from config.database import engine, Base
from models import models
from api.property import property
from api.controller import property_controller, auth_controller


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='API de Marketplace Imobiliaria',
    description='API de Marketplace Imobiliaria',
    version='0.0.1',
    docs_url='/',
    contact={
        'name': 'Xavier Francisco',
        'url': 'https://xavierfrancisco.com',
        'email': 'xavierfrancisco353@gmail.com',
    },
    license_info={
        'name': 'MIT License',
        'url': 'https://opensource.org/licenses/MIT',
    },
)

app.include_router(auth_controller.router)
app.include_router(property_controller.router)
