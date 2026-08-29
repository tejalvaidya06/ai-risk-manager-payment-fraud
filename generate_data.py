import os
import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
N = 12000

merchant_risk = RNG.beta(2, 8, N)
account_age_days = RNG.integers(1, 1800, N)
amount = np.round(np.exp(RNG.normal(np.log(180), 1.0, N)), 2)
amount = np.clip(amount, 5, 15000)
velocity_1h = RNG.poisson(1.8 + 3.5 * merchant_risk)
velocity_24h = velocity_1h + RNG.poisson(4 + 9 * merchant_risk)
distance_km = np.round(np.clip(RNG.gamma(2, 35, N), 0, 2500), 1)
device_age_days = RNG.integers(0, 1500, N)
ip_risk = np.clip(RNG.beta(2, 10, N) + merchant_risk * 0.7, 0, 1)
failed_attempts_24h = RNG.poisson(0.7 + 3.5 * merchant_risk)
chargeback_history = RNG.binomial(1, np.clip(0.02 + merchant_risk * 0.22, 0, .5))
new_device = (device_age_days < 7).astype(int)
new_account = (account_age_days < 14).astype(int)
night_txn = RNG.binomial(1, 0.22, N)
amount_deviation = np.abs(np.log1p(amount) - np.log1p(150))

logit = (
    -8.8
    + 0.55 * np.log1p(amount)
    + 0.32 * velocity_1h
    + 0.09 * velocity_24h
    + 0.00055 * distance_km
    + 2.2 * ip_risk
    + 0.32 * failed_attempts_24h
    + 1.35 * chargeback_history
    + 1.15 * new_device
    + 1.0 * new_account
    + 0.35 * night_txn
    + 0.55 * amount_deviation
    + RNG.normal(0, .7, N)
)
prob = 1 / (1 + np.exp(-logit))
fraud = RNG.binomial(1, prob)

payment_methods = RNG.choice(["card", "upi", "netbanking", "wallet"], N, p=[.42,.38,.12,.08])
channels = RNG.choice(["web", "android", "ios", "api"], N, p=[.34,.31,.20,.15])
regions = RNG.choice(["IN-MH", "IN-DL", "IN-KA", "IN-TN", "IN-GJ", "IN-WB", "IN-UP"], N)

# Small synthetic merchant/customer identifiers; not real payment data.
df = pd.DataFrame({
    "transaction_id": [f"TXN{i:07d}" for i in range(N)],
    "merchant_id": [f"M{RNG.integers(1, 401):04d}" for _ in range(N)],
    "amount": amount,
    "payment_method": payment_methods,
    "channel": channels,
    "region": regions,
    "account_age_days": account_age_days,
    "device_age_days": device_age_days,
    "velocity_1h": velocity_1h,
    "velocity_24h": velocity_24h,
    "distance_km": distance_km,
    "ip_risk": np.round(ip_risk, 4),
    "failed_attempts_24h": failed_attempts_24h,
    "chargeback_history": chargeback_history,
    "new_device": new_device,
    "new_account": new_account,
    "night_txn": night_txn,
    "fraud": fraud,
})

os.makedirs("data", exist_ok=True)
df.to_csv("data/transactions.csv", index=False)
print(f"Created {len(df):,} synthetic transactions. Fraud rate: {df.fraud.mean():.2%}")
