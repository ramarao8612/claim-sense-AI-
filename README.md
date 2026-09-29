# ClaimSense AI — MVP Scaffold

AI-assisted insurance claims review for personal auto physical-damage claims.
Backend: FastAPI · Frontend: React + TypeScript · DB: PostgreSQL + pgvector ·
Storage: MinIO (S3-compatible) · LLM: Ollama (local, free)

## Repo structure

```
claimsense-ai/
├── backend/                 # FastAPI app (Python 3.12)
│   ├── app/
│   │   ├── main.py          # App entrypoint, router wiring
│   │   ├── database.py      # SQLAlchemy engine + session
│   │   ├── models.py        # DB tables (Claim, Document, ExtractedFact,
│   │   │                    #   Analysis, PolicyChunk, Decision, AuditEvent)
│   │   ├── schemas.py       # Pydantic request/response models
│   │   ├── core/config.py   # Settings from environment variables
│   │   ├── api/             # Route handlers: claims, documents, analyses, decisions
│   │   └── services/        # Business logic:
│   │                        #   extraction.py (PyMuPDF + Tesseract)
│   │                        #   scoring.py    (severity / priority rules + ML)
│   │                        #   risk.py       (fraud-risk signals + XGBoost)
│   │                        #   rag.py        (embeddings + pgvector retrieval)
│   │                        #   summarizer.py (Ollama LLM adapter -> Bedrock later)
│   ├── tests/               # pytest
│   └── Dockerfile
├── frontend/                # React + TypeScript + Vite
│   └── src/pages/           # ClaimsQueue, NewClaim, ReviewWorkspace,
│                            # DecisionPanel, PolicyAdmin
├── data/
│   ├── raw/                 # Kaggle CSVs go here (git-ignored)
│   ├── notebooks/           # Your EDA notebooks
│   └── scripts/
│       ├── download_kaggle.py   # Downloads the free Kaggle datasets
│       ├── make_policy_pdfs.py  # Generates synthetic policy PDFs
│       └── make_invoice_pdfs.py # Generates synthetic invoice PDFs
├── infra/
│   └── aws-ec2-setup.sh     # Installs Docker on a free-tier EC2 box
├── scripts/
│   └── demo_seed.py         # Seeds the 4 demo scenarios
├── docker-compose.yml       # Runs EVERYTHING with one command
└── .github/workflows/ci.yml # Free CI: tests + lint on every push
```

## Quickstart (local, all free)

```bash
# 1. Clone YOUR repo (paste the link your friend sent you)
git clone <your-friends-repo-link>
cd claimsense-ai

# 2. Get the free datasets (~1 min)
pip install kaggle fpdf2
python data/scripts/download_kaggle.py

# 3. Generate synthetic policy + invoice PDFs
python data/scripts/make_policy_pdfs.py
python data/scripts/make_invoice_pdfs.py

# 4. Start everything
docker compose up --build

# 5. Open
#    Frontend : http://localhost:5173
#    API docs : http://localhost:8000/docs
#    MinIO    : http://localhost:9001
```

## Build order (maps to the step-by-step guide)

0. Tool installs → 1. This repo → 2. Kaggle data + EDA → 3. `docker compose up db`
4. `backend/app/api/claims.py` → 5. `services/extraction.py` → 6. `services/scoring.py`
7. `services/risk.py` → 8. `services/rag.py` → 9. `services/summarizer.py`
10. `frontend/src/pages/*` → 11. `scripts/demo_seed.py` → 12. compose → 13. AWS → 14. CI/polish

## Safety boundary (from the SDD)

AI assists the adjuster; it never approves, denies, pays, or declares fraud.
Every final decision requires a human adjuster + written rationale.
