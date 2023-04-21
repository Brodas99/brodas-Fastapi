from typing import List
from fastapi import APIRouter

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK
from app.models.user.user import User_Create, UserInDB, User_Update, UserPassword_Update, User_Out, UserPublic

from app.db.repositories.user import UserRepository
from app.api.dependencies.database import get_repository 


router = APIRouter()

@router.post("/signup/", response_model=User_Out, name="users:register-new-user", status_code=HTTP_201_CREATED)
async def register_new_user(
    user: User_Create = Body(..., embed=True),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> User_Out:

    user_create = await user_repo.register_new_user(new_user=user)
    return user_create
 
@router.get("/", response_model=List[UserPublic], status_code=HTTP_200_OK)
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

@router.get("/email/{email}/", response_model=List[UserPublic], name="users:get-user-email", status_code=HTTP_200_OK)
async def get_user_by_email(email: str, user_repo: UserRepository = Depends(get_repository(UserRepository))) -> List[UserPublic]:
    user_email = await user_repo.get_user_by_email(email=email)

    if not user_email:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="This users email does not exists")
    return user_email

@router.get("/username/{username}/", response_model=List[UserPublic], name="users:get-user-name", status_code=HTTP_200_OK)
async def get_user_by_username(username: str, user_repo: UserRepository = Depends(get_repository(UserRepository))) -> List[UserPublic]:
    user_name = await user_repo.get_user_by_username(username=username)
    if not user_name:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="This username does not exists")
    return user_name