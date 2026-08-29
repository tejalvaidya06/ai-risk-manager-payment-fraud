import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from risk_engine import score_transaction

st.set_page_config(page_title="AI Risk Manager", page_icon="🛡️", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/transactions.csv")

df = load_data()

st.title("🛡️ AI Risk Manager")
st.caption("Payment Risk Intelligence — synthetic portfolio simulation")

fraud_rate = df.fraud.mean()
approved = df.shape[0]
loss = df.loc[df.fraud.eq(1), "amount"].sum()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Transactions", f"{approved:,}")
c2.metric("Synthetic fraud rate", f"{fraud_rate:.2%}")
c3.metric("Fraud exposure", f"₹{loss:,.0f}")
c4.metric("Avg. transaction", f"₹{df.amount.mean():,.0f}")

st.divider()

left,right = st.columns([1,1])
with left:
    st.subheader("Live transaction risk scoring")
    amount = st.number_input("Amount (₹)", 5.0, 20000.0, 850.0, step=50.0)
    v1 = st.number_input("Transactions in last 1h", 0, 30, 2)
    v24 = st.number_input("Transactions in last 24h", 0, 100, 7)
    ip = st.slider("IP risk", 0.0, 1.0, .15, .01)
    distance = st.number_input("Geo distance signal (km)", 0.0, 3000.0, 35.0, step=10.0)
    failed = st.number_input("Failed attempts in 24h", 0, 30, 0)
    cb = st.checkbox("Chargeback history")
    new_device = st.checkbox("New device")
    new_account = st.checkbox("New account")
    night = st.checkbox("Night-time transaction")

    result = score_transaction({
        "amount": amount, "velocity_1h": v1, "velocity_24h": v24, "ip_risk": ip,
        "distance_km": distance, "failed_attempts_24h": failed,
        "chargeback_history": int(cb), "new_device": int(new_device),
        "new_account": int(new_account), "night_txn": int(night)
    })

with right:
    st.subheader("Decision")
    st.metric("Risk score", f"{result.risk_score}/100")
    st.metric("Estimated fraud probability", f"{result.fraud_probability:.1%}")
    if result.decision == "BLOCK":
        st.error(f"Decision: {result.decision}")
    elif result.decision == "REVIEW":
        st.warning(f"Decision: {result.decision}")
    else:
        st.success(f"Decision: {result.decision}")
    st.write("**Top risk reasons**")
    for r in result.reasons:
        st.write(f"• {r}")
    st.progress(result.risk_score / 100)
    st.info("Policy: 0–44 Approve · 45–74 Review · 75–100 Block")

st.divider()

st.subheader("Risk intelligence")
a,b = st.columns(2)
with a:
    fraud_by_method = df.groupby("payment_method", as_index=False).fraud.mean().sort_values("fraud", ascending=False)
    fig = px.bar(fraud_by_method, x="payment_method", y="fraud", title="Fraud rate by payment method")
    fig.update_yaxes(tickformat=".1%")
    st.plotly_chart(fig, use_container_width=True)
with b:
    fig2 = px.histogram(df, x="amount", color="fraud", nbins=50, title="Transaction amount distribution", log_x=True)
    st.plotly_chart(fig2, use_container_width=True)

c,d = st.columns(2)
with c:
    agg = df.groupby("velocity_1h", as_index=False).fraud.mean()
    fig3 = px.line(agg, x="velocity_1h", y="fraud", markers=True, title="Fraud rate vs. 1-hour velocity")
    fig3.update_yaxes(tickformat=".1%")
    st.plotly_chart(fig3, use_container_width=True)
with d:
    region = df.groupby("region", as_index=False).agg(fraud_rate=("fraud","mean"), volume=("fraud","size"))
    fig4 = px.scatter(region, x="volume", y="fraud_rate", size="volume", hover_name="region", title="Regional risk monitoring")
    fig4.update_yaxes(tickformat=".1%")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.subheader("Risk Manager view")
st.dataframe(df.sort_values(["fraud", "amount"], ascending=[False, False]).head(30), use_container_width=True)
