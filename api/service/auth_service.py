from datetime import timedelta, datetime
from config.database import get_db
from models import models
from jose import JWTError, jwt
from schemas import schemas
from api.repository.auth_repository import AuthRepository
from api.repository.auth_repository import bcrypt_context


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    def create_user(self, user: schemas.CreateUserRequest):
        user.password = bcrypt_context.hash(user.password)
        return self.auth_repository.create_user(user)

    def authenticate_user(self, username: str, password: str):
        user = self.auth_repository.get_user_by_username(username)
        if not user:
            return False
        if not bcrypt_context.verify(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, username: str, user_id: int, expires_delta: timedelta):
        encode = {'sub': username, 'id': user_id}
        expires = datetime.utcnow() + expires_delta
        encode.update({'exp': expires})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None