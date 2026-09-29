"""Severity & priority scoring (Guide Step 6).

Start with transparent rules you can explain to an adjuster. Later, train a
scikit-learn model on the Kaggle data and A/B it against these rules —
keep whichever you can defend.
"""


def score_claim(amount: float, incident_severity: str | None,
                claim_age_days: int, missing_docs: bool) -> dict:
    severity = "low"
    if amount >= 15000 or incident_severity == "major":
        severity = "high"
    elif amount >= 5000 or incident_severity == "moderate":
        severity = "medium"

    priority = "routine"
    if severity == "high" or (claim_age_days > 30 and missing_docs):
        priority = "urgent"
    elif severity == "medium" or missing_docs:
        priority = "elevated"

    reasons = [
        f"amount=${amount:,.0f} -> severity={severity}",
        f"claim_age={claim_age_days}d, missing_docs={missing_docs} -> priority={priority}",
    ]
    return {"severity": severity, "priority": priority,
            "confidence": 0.8, "reasons": reasons}


# TODO: train models/severity_model.joblib on Kaggle insurance_claims.csv
# (target: incident_severity) and load it here for the "pro" version.
