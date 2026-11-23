from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/deals", tags=["Creator deals"])


def owned_deal(deal_id: int, db: Session, user: models.User):
    deal = db.query(models.Deal).filter_by(id=deal_id, owner_id=user.id).first()
    if deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.post("/", response_model=schemas.DealOut, status_code=201)
def create_deal(data: schemas.DealCreate, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    deal = models.Deal(owner_id=user.id, **data.model_dump())
    db.add(deal)
    db.commit()
    db.refresh(deal)
    return deal


@router.get("/", response_model=list[schemas.DealOut])
def list_deals(stage: Optional[schemas.DealStage] = None, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    query = db.query(models.Deal).filter_by(owner_id=user.id)
    if stage is not None:
        query = query.filter_by(stage=stage)
    return query.order_by(models.Deal.id.desc()).all()


@router.get("/{deal_id}", response_model=schemas.DealOut)
def get_deal(deal_id: int, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    return owned_deal(deal_id, db, user)


@router.patch("/{deal_id}", response_model=schemas.DealOut)
def update_deal(deal_id: int, data: schemas.DealUpdate, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    deal = owned_deal(deal_id, db, user)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(deal, field, value)
    db.commit()
    db.refresh(deal)
    return deal


@router.delete("/{deal_id}", status_code=204)
def delete_deal(deal_id: int, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    deal = owned_deal(deal_id, db, user)
    db.delete(deal)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
