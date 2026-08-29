import json
import os
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

FEATURES = [
    "amount", "payment_method", "channel", "region", "account_age_days",
    "device_age_days", "velocity_1h", "velocity_24h", "distance_km", "ip_risk",
    "failed_attempts_24h", "chargeback_history", "new_device", "new_account", "night_txn"
]
TARGET = "fraud"

df = pd.read_csv("data/transactions.csv")
X, y = df[FEATURES], df[TARGET]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25, stratify=y, random_state=42)
cat = ["payment_method", "channel", "region"]
num = [c for c in FEATURES if c not in cat]
pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), cat)], remainder="passthrough")
model = HistGradientBoostingClassifier(max_depth=6, learning_rate=.08, max_iter=180, random_state=42)
# HGB needs dense features, so transform manually.
Xtr = pre.fit_transform(X_train)
Xte = pre.transform(X_test)
model.fit(Xtr, y_train)
p = model.predict_proba(Xte)[:, 1]
pred = (p >= .5).astype(int)
metrics = {
    "roc_auc": roc_auc_score(y_test, p),
    "pr_auc": average_precision_score(y_test, p),
    "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
    "classification_report": classification_report(y_test, pred, output_dict=True),
}
os.makedirs("models", exist_ok=True)
joblib.dump({"preprocessor": pre, "model": model, "features": FEATURES}, "models/risk_model.joblib")
with open("models/metrics.json", "w") as f: json.dump(metrics, f, indent=2)
print(json.dumps({k:v for k,v in metrics.items() if k in ["roc_auc","pr_auc"]}, indent=2))
print("Saved models/risk_model.joblib")
