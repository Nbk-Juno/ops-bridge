from datetime import datetime
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


class TokenData(BaseModel):
    user_id: int | None = None


class AssetStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    maintenance = "maintenance"


class AssetType(str, Enum):
    equipment = "equipment"
    personnel = "personnel"
    resource = "resource"


class AssetCreate(BaseModel):
    name: str
    asset_type: AssetType
    status: AssetStatus = AssetStatus.active
    location: str
    asset_metadata: dict | None = None


class AssetUpdate(BaseModel):
    name: str | None = None
    asset_type: AssetType | None = None
    status: AssetStatus | None = None
    location: str | None = None
    asset_metadata: dict | None = None


class AssetResponse(BaseModel):
    id: int
    owner_id: int
    name: str
    asset_type: AssetType
    status: AssetStatus
    location: str
    asset_metadata: dict | None = None
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class AuditLogResponse(BaseModel):
    id: int
    asset_id: int
    event_type: str
    payload: dict
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
