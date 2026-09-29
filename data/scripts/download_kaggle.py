"""Download the free Kaggle datasets used by ClaimSense AI (Guide Step 2).

Prereqs:
  pip install kaggle
  1. Create a Kaggle account -> Settings -> Create New API Token
  2. Save kaggle.json to ~/.kaggle/kaggle.json (chmod 600)

Run: python data/scripts/download_kaggle.py
"""
import zipfile
from pathlib import Path

from kaggle.api.kaggle_api_extended import KaggleApi

RAW = Path(__file__).resolve().parents[1] / "raw"
RAW.mkdir(parents=True, exist_ok=True)

DATASETS = {
    # ~15k claims, 33 cols, fraud label -> fraud-risk model (Step 7)
    "shivamb/vehicle-claim-fraud-detection": "vehicle_fraud",
    # ~1k claims, 40 features incl. incident_severity -> severity model (Step 6)
    "buntyshah/auto-insurance-claims-data": "auto_claims",
}

api = KaggleApi()
api.authenticate()

for slug, folder in DATASETS.items():
    dest = RAW / folder
    dest.mkdir(exist_ok=True)
    print(f"Downloading {slug} ...")
    api.dataset_download_files(slug, path=str(dest), unzip=True)
    print("  ->", sorted(p.name for p in dest.iterdir()))
print("\nDone. CSVs live in data/raw/ (git-ignored, never committed).")
