from fastapi import APIRouter, Depends, status, HTTPException, Response
#from sqlalchemy.orm import Session
from ..database import Session, get_db
from .. import schemas, models, utils

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credential: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credential.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Invalid credentials")

    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid credentials")

    return {"token": "example token"}