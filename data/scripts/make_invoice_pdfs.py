"""Generate synthetic repair-estimate PDFs from Kaggle rows (Guide Step 5).

Reads data/raw/auto_claims/insurance_claims.csv, takes a few rows, and writes
fake shop estimates as PDFs — perfect test uploads for the document pipeline.
Run: pip install fpdf2 pandas && python data/scripts/make_invoice_pdfs.py
"""
from pathlib import Path

import pandas as pd
from fpdf import FPDF

RAW = Path(__file__).resolve().parents[1] / "raw"
OUT = RAW / "invoices"
OUT.mkdir(parents=True, exist_ok=True)

csv = next((RAW / "auto_claims").glob("*.csv"))
df = pd.read_csv(csv)

for i, row in df.head(5).iterrows():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "SYNTHETIC REPAIR ESTIMATE — ACME AUTO BODY", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    amount = float(row.get("total_claim_amount", 2500) or 2500)
    pdf.multi_cell(0, 8,
        f"Claim ref: SYN-{1000 + i}\n"
        f"Vehicle: {row.get('auto_make', 'Unknown')} {row.get('auto_model', '')} {row.get('auto_year', '')}\n"
        f"Incident severity: {row.get('incident_severity', 'n/a')}\n"
        f"Labor: ${amount * 0.45:,.2f}\nParts: ${amount * 0.55:,.2f}\n"
        f"TOTAL ESTIMATE: ${amount:,.2f}\n"
        "SYNTHETIC DOCUMENT — FOR SOFTWARE TESTING ONLY")
    path = OUT / f"estimate_SYN-{1000 + i}.pdf"
    pdf.output(str(path))
    print("wrote", path)
