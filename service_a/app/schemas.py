from pydantic import BaseModel, ConfigDict, EmailStr
from enum import Enum


class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class AssetStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    maintenance = "maintenance"
