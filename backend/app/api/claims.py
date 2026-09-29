"""Claim intake endpoints (SDD: POST /claims)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/claims", tags=["claims"])


@router.post("", response_model=schemas.ClaimOut, status_code=201)
def create_claim(payload: schemas.ClaimCreate, db: Session = Depends(get_db)):
    claim = models.Claim(**payload.model_dump())
    db.add(claim)
    db.commit()
    db.refresh(claim)
    db.add(models.AuditEvent(actor="system", action="claim.created",
                             entity="claim", entity_id=str(claim.id),
                             claim_version=claim.version))
    db.commit()
    return claim


@router.get("")
def list_claims(db: Session = Depends(get_db)):
    claims = db.query(models.Claim).order_by(models.Claim.created_at.desc()).all()
    return [schemas.ClaimOut.model_validate(c) for c in claims]


@router.get("/{claim_id}", response_model=schemas.ClaimOut)
def get_claim(claim_id: str, db: Session = Depends(get_db)):
    claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()
    if not claim:
        from fastapi import HTTPException
        raise HTTPException(404, "claim not found")
    return claim
