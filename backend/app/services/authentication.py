import jwt
import bcrypt
from datetime import datetime, timedelta 
from passlib.context import CryptContext
from app.models.user.user import UserPassword_Update

from app.core.config import SECRET_KEY, JWT_ALGORITHM, JWT_AUDIENCE, JWT_TOKEN_PREFIX, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.jwt.token import JWTMeta, JWTCreds, JWTPayload
from app.models.user.user import UserPassword_Update, UserInDB

from typing import Optional
from fastapi import HTTPException, status
from pydantic import ValidationError


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
    
    def verify_password(self, *, password: str, salt: str, hashed_password: str) -> bool:
        return pwd_context.verify(password + salt, hashed_password)
    
    def create_access_token(
        self,
        *,
        user: UserInDB,
        secret_key: str = str(SECRET_KEY),
        audience: str = JWT_AUDIENCE,
        expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES,
    ) -> str:
        
        if not user or not isinstance(user, UserInDB):
            return None
        
        jwt_meta = JWTMeta(
            aud=audience,
            iat=datetime.timestamp(datetime.utcnow()),
            exp=datetime.timestamp(datetime.utcnow() + timedelta(minutes=expires_in))
        )
        
        jwt_creds = JWTCreds(sub=user.email, username=user.username)
        token_payload = JWTPayload(
            **jwt_meta.dict(),
            **jwt_creds.dict(),
        )
        access_token = jwt.encode(token_payload.dict(), secret_key, algorithm=JWT_ALGORITHM)
        return access_token
    
    def get_username_from_token(self, *, token: str, secret_key: str) -> Optional[str]:
        try:
            decoded_token = jwt.decode(token, str(secret_key), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])
            payload = JWTPayload(**decoded_token)
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload.username