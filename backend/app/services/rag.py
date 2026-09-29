"""Policy RAG: chunk -> embed -> pgvector search (Guide Step 8).

Ingestion (run once per policy version):
  1. Extract text per page (services.extraction).
  2. Split into section chunks (~400 tokens, 50 overlap).
  3. Embed with sentence-transformers 'all-MiniLM-L6-v2' (384 dims, free, local).
  4. Insert into policy_chunks with (policy_id, version, section, page).

Retrieval: embed the question, cosine-similarity search filtered by the
claim's ACTIVE policy version, return top-k chunks as citations.
"""
from sentence_transformers import SentenceTransformer

_model = None


def get_embedder():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunks.append(" ".join(words[i:i + chunk_size]))
        i += chunk_size - overlap
    return chunks


# TODO: implement ingest_policy(db, policy_id, version, pdf_bytes) and
#       retrieve(db, policy_id, version, question, k=5) using
#       PolicyChunk.embedding.cosine_distance(...) in SQLAlchemy.
