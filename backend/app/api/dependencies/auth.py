from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import SECRET_KEY, API_PREFIX
from app.models.user.user import UserInDB
from app.api.dependencies.database import get_repository
from app.db.repositories.user import UserRepository
from app.services import auth_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX}/user/login/token/")

async def get_user_from_token(
    *,
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> Optional[UserInDB]:
    try:
        username = auth_service.get_username_from_token(token=token, secret_key=str(SECRET_KEY))
        user = await user_repo.get_user_by_username(username=username)
        print(user)
    except Exception as e:
        raise e
    return user

def get_current_active_user(current_user: UserInDB = Depends(get_user_from_token)) -> Optional[UserInDB]:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="No authenticated user.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Not an active user.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user