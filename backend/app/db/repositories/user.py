from fastapi import Depends, APIRouter, HTTPException, Path, Body
from app.db.repositories.base import BaseRepository
from app.models.user.user import User_Create, UserInDB, User_Update, UserPassword_Update, User_Out, UserPublic

from app.db.repositories.queries.user import CREATE_USER_QUERY, GET_ALL_USERS_QUERY, GET_USER_BY_ID_QUERY,GET_USER_BY_EMAIL_QUERY, GET_USER_BY_USERNAME_QUERY, UPDATE_USER_BY_ID_QUERY
from typing import List
from datetime import datetime
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from fastapi.security import OAuth2PasswordRequestForm

class UserRepository(BaseRepository):
    
    def __init__(self, db) -> None:
        super().__init__(db)
    
    async def register_new_user(self, *, new_user: User_Create) -> UserInDB:

        if await self.get_user_by_email(email=new_user.email):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='This email is already registered - please sign in or double check your email'
            )
        
        if await self.get_user_by_username(username=new_user.username):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='This username is already registered - Please user another username or login'
            )
        
        creating_new_user = await self.db.fetch_one(query=CREATE_USER_QUERY, values={**new_user.dict(), "salt": "123"})
        return UserInDB(**creating_new_user)
    
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
    
    async def get_user_by_email(self, *, email: str) -> UserPublic:
        user_by_email = await self.db.fetch_all(query=GET_USER_BY_EMAIL_QUERY, values={'email':email})
        if not user_by_email:
            return None
        return [UserPublic(**user_email) for user_email in user_by_email]

    async def get_user_by_username(self, *, username: str) -> UserPublic:
        user_by_username = await self.db.fetch_all(query=GET_USER_BY_USERNAME_QUERY, values={'username':username})
        if not user_by_username:
            return None
        return [UserPublic(**user_username) for user_username in user_by_username]
    
    async def update_user_account(self, *, user_id: int, user_update: User_Update) -> UserInDB:
        user_update = await self.db.fetch_all(query = UPDATE_USER_BY_ID_QUERY, values={'id': user_id,**user_update.dict()})
        return user_update
    
    
    def update_user_password(self, *, update_user_password: User_Create) -> UserInDB:
        pass