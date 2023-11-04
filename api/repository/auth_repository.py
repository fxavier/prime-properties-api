from sqlalchemy.orm import Session
from models import models
from schemas import schemas
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: schemas.CreateUserRequest):
        db_user = models.User(
            username=user.username,
            name=user.name,
            email=user.email,
            phone=user.phone,
            hashed_password=user.password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_username(self, username: str):
        return self.db.query(models.User).filter(models.User.username == username).first()

    def get_user_by_email(self, email: str):
        return self.db.query(models.User).filter(models.User.email == email).first()
    
    def get_user_by_id(self, id: int):
        return self.db.query(models.User).filter(models.User.id == id).first()