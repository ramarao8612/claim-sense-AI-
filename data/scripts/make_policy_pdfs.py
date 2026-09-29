"""Generate 3 synthetic auto policy PDFs for the RAG corpus (Guide Step 8).

These are FAKE policies you write yourself — clearly synthetic, no real
insurer content. Run: pip install fpdf2 && python data/scripts/make_policy_pdfs.py
Output: data/raw/policies/*.pdf
"""
from pathlib import Path

from fpdf import FPDF

OUT = Path(__file__).resolve().parents[1] / "raw" / "policies"
OUT.mkdir(parents=True, exist_ok=True)

POLICIES = {
    "POL-AUTO-2026-v3": [
        ("SECTION 1 — COLLISION COVERAGE",
         "We will pay for direct and accidental loss to your covered auto caused by collision, "
         "less the applicable deductible shown in the declarations. Collision means the upset of "
         "your covered auto or its impact with another vehicle or object. The limit of liability "
         "is the lesser of the actual cash value or the cost of repair."),
        ("SECTION 2 — DEDUCTIBLE",
         "A $500 deductible applies to each collision claim. The deductible is subtracted from "
         "the amount we pay. No deductible applies to claims arising solely from glass breakage."),
        ("SECTION 3 — EXCLUSIONS",
         "We do not cover loss caused by wear and tear, freezing, mechanical or electrical "
         "breakdown, or road damage to tires. We do not cover loss to any auto used for "
         "ride-sharing or delivery services unless the ride-share endorsement is attached."),
        ("SECTION 4 — RENTAL REIMBURSEMENT",
         "If the rental reimbursement endorsement is shown in the declarations, we will pay up "
         "to $40 per day, maximum $1,200 per occurrence, for rental of a substitute auto while "
         "your covered auto is being repaired after a covered collision loss."),
        ("SECTION 5 — DUTIES AFTER A LOSS",
         "You must notify us promptly, protect the auto from further damage, permit inspection "
         "before repair, and submit a signed proof of loss within 60 days if we request it. "
         "Failure to permit inspection may result in denial of the claim."),
    ],
    "POL-AUTO-2026-v2": [
        ("SECTION 1 — COLLISION COVERAGE",
         "Prior version: deductible was $1,000 per collision claim. Rental reimbursement "
         "was capped at $30 per day, maximum $900 per occurrence."),
    ],
}


def make_pdf(policy_id: str, sections: list[tuple[str, str]]):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 12, f"SYNTHETIC AUTO POLICY {policy_id}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 8, "SYNTHETIC DOCUMENT — FOR SOFTWARE TESTING ONLY", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    for title, body in sections:
        pdf.set_font("Helvetica", "B", 12)
        pdf.multi_cell(0, 8, title)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, body)
        pdf.ln(3)
    path = OUT / f"{policy_id}.pdf"
    pdf.output(str(path))
    print("wrote", path)


for pid, sections in POLICIES.items():
    make_pdf(pid, sections)
