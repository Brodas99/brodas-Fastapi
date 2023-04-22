from typing import Optional, Union
from pydantic import EmailStr, constr
from pydantic import BaseModel, Field
from app.models.core import IDModelMixin, CoreModel
from app.models.core import DateTimeModelMixin
from datetime import datetime
from app.models.jwt.token import AccessToken

"""
MODELS IN THE FOLLOWING ORDER 

- BASE 
- CREATE
- UPDATE 
- INDB
- PUBLIC 

"""


"""
USER METADATA MODEL 
"""

class User_Base(CoreModel):
    """
    Base Layer for Users in Application
    """

    username: constr(min_length=3, regex="[a-zA-Z0-9_-]+$")
    firstname: str = Field(description="First Name of a given User")
    lastname: str = Field(description="Last Name of a given User")
    email: EmailStr = Field(description="Email Address of a given User")
    email_verified: bool = Field(default = False, description="User has verified their Email")
    is_active: bool = Field(default = True, description="User has signed-in in last 60 days")


class User_Create(CoreModel):
    """
    Email, username, and password are required for registering a new user
    """
    email: EmailStr
    firstname: str
    lastname: str
    username: constr(min_length=3, regex="[a-zA-Z0-9_-]+$")
    password: constr(min_length=7, max_length=100)


class User_Update(CoreModel):
    """
    Users are allowed to update their email and username - might have to rethink the email update and how that looks if it already exist
    """

    email: Optional[EmailStr]
    username: Optional[constr(min_length=3, regex="^[a-zA-Z0-9_-]+$")]


class UserPassword_Update(CoreModel):
    """
    Users can change their password, then convert to salt - thinking about when they do, updated_at will also be part of the update query
    """
    password: constr(min_length=7, max_length=100)
    salt: str
    #updated_at: Optional[datetime]


class UserInDB(IDModelMixin, DateTimeModelMixin, User_Base):
    """
    Add into db id, created_at, updated_at, and user's password and salt_password and all in base model
    """

    password: constr(min_length=7, max_length=100)
    salt: str


class UserPublic(IDModelMixin, DateTimeModelMixin, User_Base):
    """
    Public to the client id, created_at, updated_at, and all in base model
    """

    access_token: Optional[AccessToken]


class User_Out(CoreModel):

    username: str
    email: EmailStr