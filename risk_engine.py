from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
import numpy as np

@dataclass
class RiskResult:
    risk_score: int
    fraud_probability: float
    decision: str
    reasons: List[str]
    rule_score: int


def _clamp(x, lo=0, hi=100):
    return int(max(lo, min(hi, round(x))))


def score_transaction(txn: Dict) -> RiskResult:
    """Hybrid demo risk engine: deterministic signals + calibrated-looking ML-style score.
    This function is intentionally self-contained so the dashboard works without a model file.
    """
    amount = float(txn.get("amount", 0))
    velocity_1h = int(txn.get("velocity_1h", 0))
    velocity_24h = int(txn.get("velocity_24h", 0))
    ip_risk = float(txn.get("ip_risk", 0))
    distance = float(txn.get("distance_km", 0))
    failed = int(txn.get("failed_attempts_24h", 0))
    cb = int(txn.get("chargeback_history", 0))
    new_device = int(txn.get("new_device", 0))
    new_account = int(txn.get("new_account", 0))
    night = int(txn.get("night_txn", 0))

    reasons = []
    rule = 0
    if velocity_1h >= 8:
        rule += 24; reasons.append("Very high transaction velocity in the last hour")
    elif velocity_1h >= 5:
        rule += 12; reasons.append("Elevated transaction velocity in the last hour")
    if velocity_24h >= 25:
        rule += 14; reasons.append("Unusually high 24-hour transaction volume")
    if ip_risk >= .70:
        rule += 22; reasons.append("High-risk IP signal")
    elif ip_risk >= .45:
        rule += 10; reasons.append("Elevated IP risk signal")
    if distance >= 1000:
        rule += 15; reasons.append("Large geographic distance signal")
    if failed >= 6:
        rule += 14; reasons.append("Multiple failed attempts")
    if cb:
        rule += 15; reasons.append("Previous chargeback history")
    if new_device:
        rule += 8; reasons.append("New device")
    if new_account:
        rule += 9; reasons.append("Very new account")
    if amount >= 5000:
        rule += 8; reasons.append("High-value transaction")
    if night:
        rule += 3; reasons.append("Night-time transaction")

    raw = (
        -5.2
        + 0.38 * np.log1p(amount)
        + 0.17 * velocity_1h
        + 0.055 * velocity_24h
        + 2.0 * ip_risk
        + 0.13 * failed
        + 0.95 * cb
        + 0.75 * new_device
        + 0.7 * new_account
        + 0.00035 * distance
        + 0.18 * night
    )
    p = float(1 / (1 + np.exp(-raw)))
    score = _clamp(100 * (0.70 * p + 0.30 * min(rule, 100) / 100))

    if score >= 75:
        decision = "BLOCK"
    elif score >= 45:
        decision = "REVIEW"
    else:
        decision = "APPROVE"

    if not reasons:
        reasons = ["No major risk signals detected"]
    return RiskResult(score, p, decision, reasons[:5], min(rule, 100))
