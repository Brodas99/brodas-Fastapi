from fastapi import Depends, APIRouter, HTTPException, Path, Body
from typing import List, Optional
from pydantic import EmailStr, constr

from app.db.repositories.base import BaseRepository
from app.models.user.user import User_Create, UserInDB, User_Update, UserPassword_Reset, User_Out, UserPublic
from app.models.jwt.token import AccessToken
from app.db.repositories.queries.user import (
    CREATE_USER_QUERY, 
    GET_ALL_USERS_QUERY, 
    GET_USER_BY_ID_QUERY,
    GET_USER_BY_EMAIL_QUERY, 
    GET_USER_BY_USERNAME_QUERY, 
    UPDATE_USER_BY_ID_QUERY,
    RESET_AND_UPDATE_USER_PASSWORD_QUERY
    )
from app.services import auth_service, email_service

from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND


class UserRepository(BaseRepository):
    
    def __init__(self, db) -> None:
        super().__init__(db)
        self.auth_service = auth_service
        self.email_service = email_service

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
        user_email = await self.db.fetch_one(query=GET_USER_BY_EMAIL_QUERY, values={'email':str(email)})
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
    
    
    async def initiate_reset_user_password(self, *, email: str):
        user = await self.get_user_by_email(email=email)

        if not user:
            return None
        
        reset = AccessToken(access_token=auth_service.create_access_token(user=user), token_type="bearer")
        self.email_service.send_email(subject='Hey Bryan', body=f'Auth Code {reset.access_token}', receiver_email="b.rodasdiaz@gmail.com")
        return True
        
    async def reset_user_password(self, *, new_password: UserPassword_Reset):
        ## after verifying that they do exists, we still create a new salt and hashed password for them
        user_password_reset = self.auth_service.create_salt_and_hashed_password(password=new_password.password)
        ## db_user_password_reset = await self.db.fetch_one(query=RESET_AND_UPDATE_USER_PASSWORD_QUERY, values=user_password_reset.dict())