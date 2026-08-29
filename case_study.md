# Case Study: AI Risk Manager

## Problem
Payment businesses need to minimize fraud while maintaining high legitimate-payment acceptance. A model that maximizes recall can still be commercially poor if it creates too many false positives.

## Proposed solution
A hybrid risk engine with four stages:

1. **Signal layer** — amount, velocity, IP risk, device age, account age, failed attempts, chargeback history and behavioral context.
2. **Detection layer** — ML fraud probability plus deterministic rules.
3. **Decision layer** — risk score and action thresholds.
4. **Monitoring layer** — fraud rate, exposure, approval/review/block rates and segment-level performance.

## Why hybrid?
Rules are useful for obvious patterns and provide operational transparency. ML captures interactions that rules can miss. Combining them gives a practical balance between coverage and explainability.

## What I would improve next
- Train on temporal splits to prevent leakage.
- Add calibrated probabilities and expected-loss optimization.
- Add graph features for shared devices, cards, IPs and merchant relationships.
- Build online velocity features with a low-latency store.
- Add analyst feedback as labels.
- Monitor drift with PSI/feature distributions and performance by cohort.
- Add model governance: model cards, versioning, audit logs and rollback.
- Run threshold experiments using expected cost of fraud, review operations and false declines.
