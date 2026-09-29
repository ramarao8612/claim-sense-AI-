"""Fraud-risk indicator (Guide Step 7). ADVISORY ONLY.

Two layers:
  1. Transparent rule signals (always shown with reason codes).
  2. XGBoost model trained on the Kaggle vehicle-claim-fraud dataset
     (saved to models/risk_xgb.joblib) — blended with the rules.

The API must ALWAYS return reason codes alongside the score, so an
adjuster can verify rather than trust.
"""

RULE_SIGNALS = {
    "claim_within_7d_of_policy_start": 0.25,
    "four_or_more_past_claims": 0.20,
    "no_police_report": 0.15,
    "no_witness": 0.10,
    "address_changed_near_claim": 0.20,
    "high_value_vehicle": 0.10,
}


def rule_signals(features: dict) -> list[dict]:
    """features: dict like {'days_policy_to_claim': 3, 'past_claims': 5, ...}"""
    triggered = []
    checks = {
        "claim_within_7d_of_policy_start": features.get("days_policy_to_claim", 999) <= 7,
        "four_or_more_past_claims": features.get("past_claims", 0) >= 4,
        "no_police_report": not features.get("police_report_filed", True),
        "no_witness": not features.get("witness_present", True),
        "address_changed_near_claim": features.get("address_change_near_claim", False),
        "high_value_vehicle": features.get("vehicle_price", 0) > 69000,
    }
    for code, hit in checks.items():
        if hit:
            triggered.append({"code": code, "weight": RULE_SIGNALS[code]})
    return triggered


def score_risk(features: dict) -> dict:
    signals = rule_signals(features)
    rule_score = min(1.0, sum(s["weight"] for s in signals))
    # TODO: load models/risk_xgb.joblib, get ml_score, blend: 0.5*rule + 0.5*ml
    ml_score = None
    final = rule_score if ml_score is None else round(0.5 * rule_score + 0.5 * ml_score, 3)
    band = "low" if final < 0.35 else ("medium" if final < 0.65 else "high")
    return {"risk_score": round(final, 3), "risk_band": band,
            "reasons": signals, "model_version": "rules-v0.1"}
