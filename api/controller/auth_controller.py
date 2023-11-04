from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from config.database import get_db
from schemas import schemas
from api.repository.auth_repository import AuthRepository
from api.service.auth_service import AuthService


router = APIRouter(
    prefix='/api/v1/auth',
    tags=['auth']
)

db_dependency = Annotated[Session, Depends(get_db)]
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# Dependency
def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(AuthRepository(db))

@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: schemas.CreateUserRequest, db: db_dependency):
    auth_repository = AuthRepository(db)
    auth_service = AuthService(auth_repository)
    return auth_service.create_user(create_user_request)

@router.post("/token", response_model=schemas.Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    auth_repository = AuthRepository(db)
    auth_service = AuthService(auth_repository)
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    token = auth_service.create_access_token(user.username, user.id, timedelta(minutes=10))
    return {'access_token': token, 'token_type': 'bearer'}


# Dependency
async def get_current_user(token: str = Depends(oauth2_bearer), auth_service: AuthService = Depends(get_auth_service)):
    payload = auth_service.decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user_id: int = payload.get("id")
    user = auth_service.auth_repository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/me", response_model=schemas.UserBase, status_code=status.HTTP_200_OK)
async def read_current_user(current_user: schemas.UserBase = Depends(get_current_user)):
    return current_user
