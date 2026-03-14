from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, Column, JSON
from database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, nullable=False)
    event_type = Column(String)  # asset.created | asset.updated | asset.deleted
    payload = Column(JSON)  # snapshot of asset at time of event
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
