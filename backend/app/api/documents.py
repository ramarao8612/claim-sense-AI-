"""Document upload + extraction pipeline (SDD: POST /claims/{id}/documents).

TODO (Step 5 of the guide):
  1. Validate file (pdf/png/jpg, <25MB).
  2. SHA-256 checksum -> reject exact duplicates.
  3. Upload bytes to MinIO/S3, save Document row (extraction_status=pending).
  4. Extract text per page with services.extraction.extract_pages().
  5. Write ExtractedFact rows with (field, value, confidence, page).
  6. Set extraction_status=done and write an audit event.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/claims", tags=["documents"])


@router.post("/{claim_id}/documents")
def upload_document(claim_id: str):
    return {"todo": "implement upload pipeline (see module docstring)", "claim_id": claim_id}
