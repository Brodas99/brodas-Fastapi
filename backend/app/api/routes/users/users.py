from typing import List
from fastapi import APIRouter

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK
from app.models.user.user import User_Create, UserInDB, User_Update, UserPassword_Update, User_Out, UserPublic

from app.db.repositories.user import UserRepository
from app.api.dependencies.database import get_repository 


router = APIRouter()

@router.post("/signup/", response_model=User_Out, name="users:register-new-user", status_code=HTTP_201_CREATED)
async def create_new_user(
    user: User_Create = Body(..., embed=True),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> User_Out:

    user_create = await user_repo.create_new_user(new_user=user)
    return user_create
 
@router.get("/", response_model=List[UserPublic], status_code=HTTP_200_OK)
async def get_all_users(user_repo: UserRepository = Depends(get_repository(UserRepository))) -> List[UserPublic]:
    user = await user_repo.get_all_users()
    
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Currently no users")
    return await user_repo.get_all_users()

@router.get("/{id}", response_model=List[UserPublic], status_code=HTTP_200_OK)
async def get_user_by_id(id: int, user_repo: UserRepository = Depends(get_repository(UserRepository))) -> List[UserPublic]:
    user = await user_repo.get_user_by_id(id=id)

    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="This user ID does not exists")
    return user

@router.get("/{email}/", response_model=List[UserPublic], status_code=HTTP_200_OK)
async def get_user_by_email(email: str, user_repo: UserRepository = Depends(get_repository(UserRepository))) -> List[UserPublic]:
    user = await user_repo.get_user_by_email(email=email)

    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="This user ID does not exists")
    return user