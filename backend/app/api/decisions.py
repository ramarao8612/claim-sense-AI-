"""Human decision endpoint (SDD: POST /claims/{id}/decisions).

Safety rule: the API refuses a decision without a human adjuster id and a
written rationale. AI output is advisory; this row is the only thing that
changes a claim's disposition.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/claims", tags=["decisions"])


@router.post("/{claim_id}/decisions", status_code=201)
def record_decision(claim_id: str, payload: schemas.DecisionCreate,
                    db: Session = Depends(get_db)):
    claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(404, "claim not found")
    decision = models.Decision(claim_id=claim.id, claim_version=claim.version,
                               action=payload.action, rationale=payload.rationale,
                               recorded_by=payload.recorded_by)
    claim.status = "decided"
    db.add(decision)
    db.add(models.AuditEvent(actor=payload.recorded_by, action=f"decision.{payload.action}",
                             entity="claim", entity_id=str(claim.id),
                             claim_version=claim.version))
    db.commit()
    return {"decision_id": str(decision.id), "action": decision.action}
