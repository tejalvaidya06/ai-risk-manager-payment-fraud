# 5-Minute Pitch — AI Risk Manager

## 0:00–0:35 — Hook
"In payments, the hardest problem isn't simply detecting fraud. It's deciding when to approve a genuine customer, when to ask for review, and when to stop a risky payment — without creating unnecessary friction.

So I built AI Risk Manager, a hybrid payment-risk decisioning platform. It turns transaction signals into a 0-to-100 risk score, an operational decision, and an explanation a risk analyst can understand."

## 0:35–1:20 — Business problem
"A binary fraud classifier is not enough for a payment company. Fraud is usually imbalanced, fraud patterns change, and false positives have a real business cost because a good customer can be blocked.

I therefore designed the project around four layers: signals, detection, decision policy, and monitoring."

## 1:20–2:10 — Product demo
"Here is the live transaction simulator. I can change amount, velocity, IP risk, failed attempts, device age, account age and chargeback history.

A normal payment receives a low score and is approved. If I increase velocity and IP risk and add a new device, the score moves upward and the system can route the transaction to review or block it.

The important part is the explanation: the system tells the analyst which signals caused the risk, rather than returning an unexplained number."

## 2:10–3:10 — Technical design
"The engine is hybrid. Deterministic rules handle high-confidence risk patterns, while the machine-learning layer estimates fraud probability from behavioral and transaction features.

The score combines those signals and the policy layer maps the score to APPROVE, REVIEW, or BLOCK. Keeping the policy separate means a risk team can tune thresholds without rebuilding the model."

## 3:10–4:05 — Analytics & measurement
"The dashboard tracks fraud rate, exposure, transaction volume, payment-method risk, velocity relationships and regional monitoring.

For evaluation I focus on ROC-AUC and especially PR-AUC because fraud is an imbalanced classification problem. But model metrics are only part of success. I would optimize against fraud loss prevented, false-positive rate, approval rate, review rate and customer friction."

## 4:05–4:45 — Production thinking
"If I took this to production, I would add streaming feature computation, feature-store consistency, model versioning, shadow deployment, drift detection, champion-challenger models, analyst feedback loops and threshold optimization based on expected business cost.

I would also monitor fairness and segment-level false positives so that an improvement in fraud recall doesn't silently damage legitimate customer acceptance."

## 4:45–5:00 — Close
"The key idea is simple: I didn't build only a fraud model. I built a risk decisioning system. That distinction is what I would bring to a fintech risk team — combining machine learning with business judgment, explainability and measurable operational outcomes."
