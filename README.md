# AI Risk Manager — Payment Fraud & Risk Intelligence Platform

A production-style portfolio project for a fintech Risk/ML role. It demonstrates how an AI Risk Manager can combine **real-time transaction signals, deterministic rules, machine learning, explainability, and risk-based actions** to reduce fraud while protecting genuine customers.

> Note: This is a portfolio simulation built with synthetic data. It does not use Razorpay internal data, rules, models, APIs, or confidential information.

## Why this project stands out

Instead of only predicting `fraud = 0/1`, the system answers the business question:

**"What should we do with this payment right now, and why?"**

It produces:
- 0–100 risk score
- APPROVE / REVIEW / BLOCK decision
- top reasons behind the decision
- model probability + rule signals
- merchant/customer-level risk views
- threshold and cost analysis
- monitoring metrics for model drift and operational performance

## Architecture

```text
Synthetic Transactions
        |
        v
Feature Engineering
(device, velocity, amount, geo, account age, payment signals)
        |
        +-------------------+
        |                   |
        v                   v
 Rule Engine          ML Risk Model
        |                   |
        +---------+---------+
                  v
          Risk Score Layer
                  |
        +---------+---------+
        |         |         |
     APPROVE    REVIEW    BLOCK
                  |
                  v
        Explainability + Dashboard
```

## Project structure

```text
ai-risk-manager/
├── app.py                 # Streamlit dashboard
├── risk_engine.py         # rules + scoring + explanations
├── train_model.py         # trains and evaluates model
├── generate_data.py       # creates realistic synthetic payment data
├── requirements.txt
├── README.md
├── pitch_script.md
├── case_study.md
└── data/
    └── transactions.csv   # generated sample data
```

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python generate_data.py
python train_model.py
streamlit run app.py
```

Then open the local Streamlit URL shown in your terminal.

## Risk decision logic

The demo intentionally uses a hybrid approach:

1. **Rules** catch high-confidence patterns such as extreme velocity or impossible geo movement.
2. **ML** estimates fraud probability from transaction behavior.
3. **Risk score** combines model probability with rule severity.
4. **Action policy** converts the score into an operational decision.
5. **Explainability** shows the strongest contributing signals.

This design is more realistic for payments than blindly trusting a single classifier.

## Evaluation

The training script reports:
- ROC-AUC
- Precision
- Recall
- F1
- confusion matrix
- PR-AUC

The case study also discusses why accuracy alone is a weak metric for imbalanced fraud data.

## Business KPIs to discuss in an interview

- Fraud loss prevented
- False-positive rate
- Approval rate
- Review rate
- Chargeback/fraud rate
- Precision at BLOCK threshold
- Recall at BLOCK threshold
- Customer friction
- Risk-adjusted payment acceptance

## Interview talking point

"I designed the project around the decision layer, not just the model. A fraud model that catches everything but blocks good customers is not a successful payment-risk system. My architecture separates detection, scoring, action policy, and monitoring so thresholds can be tuned against business costs."
