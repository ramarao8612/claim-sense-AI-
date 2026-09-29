"""Analysis endpoints (SDD: POST /claims/{id}/analyses, GET /analyses/{id}).

TODO (Steps 6-9 of the guide):
  1. Load claim + extracted facts for the claim's current version.
  2. severity/priority  <- services.scoring.score_claim(...)
  3. risk_score/reasons <- services.risk.score_risk(...)   (advisory only)
  4. policy citations   <- services.rag.retrieve(...)
  5. summary            <- services.summarizer.summarize(...)
  6. Persist one Analysis row (never update in place) + audit event.
"""
from fastapi import APIRouter

router = APIRouter(tags=["analyses"])


@router.post("/claims/{claim_id}/analyses")
def start_analysis(claim_id: str):
    return {"todo": "implement analysis pipeline (see module docstring)", "claim_id": claim_id}


@router.get("/analyses/{analysis_id}")
def get_analysis(analysis_id: str):
    return {"todo": "return stored Analysis row", "analysis_id": analysis_id}


@router.get("/analyses/{analysis_id}/citations/{chunk_id}")
def get_citation(analysis_id: str, chunk_id: str):
    return {"todo": "return the PolicyChunk source text", "chunk_id": chunk_id}
