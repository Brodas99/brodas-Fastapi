from typing import List
from fastapi import APIRouter

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED,HTTP_404_NOT_FOUND
from app.core.config import SECRET_KEY
from app.api.dependencies.auth import get_current_active_user
from app.models.user.user import User_Create, UserInDB, User_Update, UserPassword_Reset, UserPassword_Update, PasswordResetRequest, User_Out, UserPublic

from app.db.repositories.user import UserRepository
from app.api.dependencies.database import get_repository 

from app.models.jwt.token import AccessToken
from app.services import auth_service
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

@router.post("/signup/", response_model=UserPublic, name="users:register-new-user", status_code=HTTP_201_CREATED)
async def register_new_user(
    new_user: User_Create = Body(..., embed=True),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserPublic:

    user_created = await user_repo.register_new_user(new_user=new_user)
    access_token = AccessToken(
        access_token=auth_service.create_access_token(user=user_created), token_type="bearer"
    )
    return UserPublic(**user_created.dict(), access_token=access_token) ##user_create
 
@router.post("/login/token/", response_model=AccessToken, name="users:login-email-and-password")
async def user_login_with_email_and_password(
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
) -> AccessToken:
    user = await user_repo.authenticate_user(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Authentication was unsuccessful.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = AccessToken(access_token=auth_service.create_access_token(user=user, expires_in=60), token_type="bearer")
    return access_token
    
@router.post('/initiate-reset-password', response_model=dict, name="users:initiate-set-password")
async def initiate_reset_user_password(
    email: str, 
    user_repo: UserRepository = Depends(get_repository(UserRepository))
) -> str:
    email = await user_repo.initiate_reset_user_password(email=email)
    if not email:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Authentication was unsuccessful.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Password reset initiated"}


@router.post("/reset-password/{token}", response_model=dict, name="users:complete-reset-password")
async def reset_user_password(
    token: str, 
    new_password: UserPassword_Reset,
    user_repo: UserRepository = Depends(get_repository(UserRepository))
) -> dict:
    
    username_from_token = auth_service.get_username_from_token(token=token, secret_key=str(SECRET_KEY))
    if not username_from_token:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    await user_repo.reset_user_password(user=username_from_token, new_password=new_password)
    return {"message": "Password reset Set"}


@router.get("/users", response_model=List[UserPublic], status_code=HTTP_200_OK)
async def get_all_users(user_repo: UserRepository = Depends(get_repository(UserRepository))) -> List[UserPublic]:
    user = await user_repo.get_all_users()
    
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Currently no users")
    return await user_repo.get_all_users()

@router.get("/id/{id}/", response_model=List[UserPublic], name="users:get-user-id", status_code=HTTP_200_OK)
async def get_user_by_id(id: int, user_repo: UserRepository = Depends(get_repository(UserRepository))) -> List[UserPublic]:
    user = await user_repo.get_user_by_id(id=id)

    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="This user ID does not exists")
    return user

@router.get("/email/{email}/", response_model=UserPublic, name="users:get-user-email", status_code=HTTP_200_OK)
async def get_user_by_email(email: str, user_repo: UserRepository = Depends(get_repository(UserRepository))) -> UserPublic:
    user_email = await user_repo.get_user_by_email(email=email)

    if not user_email:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="This users email does not exists")
    return user_email

@router.get("/username/{username}/", response_model=UserPublic, name="users:get-user-name", status_code=HTTP_200_OK)
async def get_user_by_username(username: str, user_repo: UserRepository = Depends(get_repository(UserRepository)), current_user: UserInDB = Depends(get_current_active_user)) -> List[UserPublic]:
    user_name = await user_repo.get_user_by_username(username=username)
    if not user_name:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="This username does not exists")
    return user_name

@router.get("/me/", response_model=UserPublic, name="users:get-current-user")
async def get_currently_authenticated_user(current_user: UserInDB = Depends(get_current_active_user)) -> UserPublic:
    return current_user
