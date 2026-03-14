from app.publisher import publish_event
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import (
    AssetCreate,
    AssetResponse,
    AssetUpdate,
)
from app.models import Asset, User
from app.dependencies import get_current_user

router = APIRouter(prefix="/assets", tags=["assets"])


@router.post("/", response_model=AssetResponse)
async def create(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_asset = Asset(**asset.model_dump(), owner_id=current_user.id)

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    publish_event("asset.created", AssetResponse.model_validate(new_asset).model_dump(mode="json"))

    return new_asset


@router.get("/", response_model=list[AssetResponse])
async def list_all_assets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Asset).all()


@router.get("/{id}", response_model=AssetResponse)
async def get_asset(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    asset = db.query(Asset).filter(Asset.id == id).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    return asset


@router.patch("/{id}", response_model=AssetResponse)
async def update_asset(
    updated_asset: AssetUpdate,
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    asset = db.query(Asset).filter(Asset.id == id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    for field, value in updated_asset.model_dump(exclude_unset=True).items():
        setattr(asset, field, value)

    db.commit()
    db.refresh(asset)

    publish_event("asset.updated", AssetResponse.model_validate(asset).model_dump(mode="json"))

    return asset


@router.delete("/{id}")
async def delete_asset(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    asset = db.query(Asset).filter(Asset.id == id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    name = asset.name
    payload = AssetResponse.model_validate(asset).model_dump(mode="json")

    db.delete(asset)
    db.commit()

    publish_event("asset.deleted", payload)

    return {"message": f"{name} deleted successfully"}
