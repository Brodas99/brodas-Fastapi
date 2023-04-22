from fastapi import Depends, APIRouter, HTTPException, Path, Body
from app.db.repositories.base import BaseRepository
from app.models.user.user import User_Create, UserInDB, User_Update, UserPassword_Update, User_Out, UserPublic
from app.services import auth_service  
from typing import Optional
from pydantic import EmailStr, constr

from app.db.repositories.queries.user import (
    CREATE_USER_QUERY, 
    GET_ALL_USERS_QUERY, 
    GET_USER_BY_ID_QUERY,
    GET_USER_BY_EMAIL_QUERY, 
    GET_USER_BY_USERNAME_QUERY, 
    UPDATE_USER_BY_ID_QUERY
    )
from typing import List
from datetime import datetime
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from databases import Database  
from fastapi.security import OAuth2PasswordRequestForm


class UserRepository(BaseRepository):
    
    def __init__(self, db) -> None:
        super().__init__(db)
        self.auth_service = auth_service

    async def register_new_user(self, *, new_user: User_Create) -> UserInDB:

        ## verify email does not exists
        if await self.get_user_by_email(email=new_user.email):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='This email is already registered - please sign in or double check your email'
            )
        
        ## verify email does not username
        if await self.get_user_by_username(username=new_user.username):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='This username is already registered - Please user another username or login'
            )
        
        ## after verifying that they do not exists, we still create a salt and hashed password for them
        user_password_update = self.auth_service.create_salt_and_hashed_password(password=new_user.password)
        
        ## the copy method will copy the dict values and change the copied model with the updated values
        ## recall, new_user is a User_Create Model
        new_user_params = new_user.copy(update=user_password_update.dict())
        creating_new_user = await self.db.fetch_one(query=CREATE_USER_QUERY, values=new_user_params.dict())
        return UserInDB(**creating_new_user)
    
    async def authenticate_user(self, *, email: EmailStr, password: str) -> Optional[UserInDB]:
        ## verify user is in DB
        user = await self.get_user_by_email(email=email)
        if not user:
            return None
        # if submitted password doesn't match
        print(f'hey bryan:  {self.auth_service.verify_password(password=password, salt=user.salt, hashed_password=user.password)}')
        if not self.auth_service.verify_password(password=password, salt=user.salt, hashed_password=user.password):
            return None
        return user

    async def get_all_users(self) -> UserPublic:
        get_all_users = await self.db.fetch_all(query=GET_ALL_USERS_QUERY)
        if not get_all_users:
            return None
        return [UserPublic(**user) for user in get_all_users]
    

    async def get_user_by_id(self, *, id: int) -> UserPublic:
        user_by_id = await self.db.fetch_all(query=GET_USER_BY_ID_QUERY, values={'id':id})
        if not user_by_id:
            return None
        return [UserPublic(**user_id) for user_id in user_by_id]   
    
    
    async def get_user_by_email(self, *, email: str) -> UserInDB:
        user_email = await self.db.fetch_one(query=GET_USER_BY_EMAIL_QUERY, values={'email':email})
        if not user_email:
            return None
        return UserInDB(**user_email)


    async def get_user_by_username(self, *, username: str) -> UserInDB:
        user_by_username = await self.db.fetch_one(query=GET_USER_BY_USERNAME_QUERY, values={'username':username})
        if not user_by_username:
            return None
        return UserInDB(**user_by_username)
    
    async def update_user_account(self, *, user_id: int, user_update: User_Update) -> UserInDB:
        user_update = await self.db.fetch_all(query = UPDATE_USER_BY_ID_QUERY, values={'id': user_id,**user_update.dict()})
        return user_update
    
    
    def update_user_password(self, *, update_user_password: User_Create) -> UserInDB:
        pass