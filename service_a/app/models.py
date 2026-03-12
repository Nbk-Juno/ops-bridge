from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String, Integer, DateTime, Column, JSON
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_pw = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    asset_type = Column(String, nullable=False)  # equipment | personnel | resource
    status = Column(String, default="active")  # active | inactive | maintenance
    location = Column(String, nullable=False)
    asset_metadata = Column(JSON)  # flexible field for extra details
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, nullable=False)
    event_type = Column(String)  # asset.created | asset.updated | asset.deleted
    payload = Column(JSON)  # snapshot of asset at time of event
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
