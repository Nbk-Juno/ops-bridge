from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import AuditLog, User
from app.dependencies import get_current_user
from app.schemas import AuditLogResponse

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/", response_model=list[AuditLogResponse])
async def get_all_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(AuditLog).all()


@router.get("/{asset_id}", response_model=list[AuditLogResponse])
async def get_assetId_logs(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = db.query(AuditLog).filter(AuditLog.asset_id == asset_id).all()

    return log
