import bcrypt

from passlib.context import CryptContext
from app.models.user.user import UserPassword_Update

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthException(BaseException):
    """
    Custom auth exception that can be modified later on.
    """
    pass

class AuthService:
    def create_salt_and_hashed_password(self, *, password):
        salt = self.generate_salt()
        hashed_password = self.hash_password(password=password, salt=salt)
        return UserPassword_Update(password=hashed_password, salt=salt)
    
    def generate_salt(self):
        return bcrypt.gensalt().decode()
        
    def hash_password(self, *, password: str, salt: str):
        return pwd_context.hash(password + salt)
    
    def verify_password(self, *, password: str, salt: str, hased_password: str) -> bool:
        return pwd_context.verify(password + salt, hased_password)