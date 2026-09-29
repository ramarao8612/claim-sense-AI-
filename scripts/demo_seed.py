"""Seed the 4 demo scenarios from the SDD (Guide Step 11).

Run AFTER the backend is up: python scripts/demo_seed.py
Creates: normal claim, high-severity claim, missing-documents claim,
conflicting-info claim — then prints their IDs for the demo script.
"""
import httpx

BASE = "http://localhost:8000"

SCENARIOS = [
    {"policy_number": "POL-100234", "loss_date": "2026-09-01T10:00:00",
     "loss_type": "collision", "description": "Rear-ended at a stoplight, bumper damage.",
     "amount": 2400, "label": "normal"},
    {"policy_number": "POL-100235", "loss_date": "2026-09-10T18:30:00",
     "loss_type": "collision", "description": "Highway multi-vehicle pileup, airbags deployed.",
     "amount": 28500, "label": "high-severity"},
    {"policy_number": "POL-100236", "loss_date": "2026-09-12T09:00:00",
     "loss_type": "theft", "description": "Vehicle stolen from driveway overnight.",
     "amount": 19000, "label": "missing-documents"},
    {"policy_number": "POL-100237", "loss_date": "2026-09-02T14:00:00",
     "loss_type": "collision", "description": "Driver says parked and hit; invoice shows 40mph impact damage.",
     "amount": 8700, "label": "conflicting-info"},
]

for s in SCENARIOS:
    label = s.pop("label")
    r = httpx.post(f"{BASE}/claims", json=s, timeout=30)
    r.raise_for_status()
    print(f"{label:18s} -> {r.json()['id']}")
