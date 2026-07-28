"""GRC Risk & Compliance Dashboard — Streamlit app.

Run with:
    streamlit run app/dashboard.py
"""
from __future__ import annotations

import sqlite3
from datetime import date
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DB_PATH = Path(__file__).resolve().parents[1] / "db" / "risk_register.db"

st.set_page_config(page_title="GRC Risk & Compliance Dashboard", layout="wide", page_icon="🛡️")


@st.cache_data(ttl=60)
def load_data():
    conn = sqlite3.connect(DB_PATH)
    risks = pd.read_sql("SELECT * FROM risks", conn)
    actions = pd.read_sql("SELECT * FROM remediation_actions", conn)
    kris = pd.read_sql("SELECT * FROM kri_snapshots", conn)
    conn.close()

    risks["inherent_risk"] = risks["likelihood"] * risks["impact"]
    risks["residual_risk"] = (risks["inherent_risk"] * (1 - risks["control_effectiveness"])).round(1)
    return risks, actions, kris


def main():
    st.title("🛡️ GRC Risk & Compliance Dashboard")
    st.caption(
        "Synthetic sample data — modeled on an enterprise risk register (RSA Archer / "
        "ServiceNow GRC style). Not real organizational data."
    )

    risks, actions, kris = load_data()

    open_risks = risks[risks.status.isin(["Open", "Mitigating"])]
    overdue_actions = actions[actions.status == "Overdue"]
    overdue_rate = len(overdue_actions) / len(actions) * 100 if len(actions) else 0
    avg_residual = open_risks.residual_risk.mean() if len(open_risks) else 0
    high_residual = open_risks[open_risks.residual_risk >= 12]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Open Risks", len(open_risks))
    c2.metric("High Residual Risk (≥12)", len(high_residual))
    c3.metric("Overdue Remediation", f"{len(overdue_actions)} ({overdue_rate:.0f}%)")
    c4.metric("Avg Residual Risk", f"{avg_residual:.1f} / 25")

    st.divider()

    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.subheader("Risk Heatmap — Likelihood × Impact")
        heat = risks.groupby(["likelihood", "impact"]).size().reset_index(name="count")
        fig = px.density_heatmap(
            heat, x="impact", y="likelihood", z="count",
            color_continuous_scale="OrRd", nbinsx=5, nbinsy=5,
            labels={"impact": "Impact", "likelihood": "Likelihood"},
        )
        fig.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("Risks by Category")
        by_cat = risks.category.value_counts().reset_index()
        by_cat.columns = ["category", "count"]
        fig2 = px.pie(by_cat, names="category", values="count", hole=0.5)
        fig2.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("KRI Trends (last 7 months)")
    metric_choice = st.selectbox("Metric", sorted(kris.metric_name.unique()))
    metric_df = kris[kris.metric_name == metric_choice].sort_values("snapshot_date")
    fig3 = px.line(
        metric_df, x="snapshot_date", y="value", markers=True,
        labels={"snapshot_date": "Month", "value": metric_df.unit.iloc[0] if len(metric_df) else ""},
    )
    fig3.add_hline(
        y=metric_df.threshold.iloc[0] if len(metric_df) else 0,
        line_dash="dash", line_color="red", annotation_text="Threshold",
    )
    fig3.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    st.subheader("⚠️ Overdue Remediation Actions")
    if len(overdue_actions):
        merged = overdue_actions.merge(risks[["risk_id", "title", "category"]], on="risk_id", how="left")
        st.dataframe(
            merged[["action_id", "title", "description", "owner", "due_date", "category"]]
            .rename(columns={"title": "risk_title"})
            .sort_values("due_date"),
            use_container_width=True, hide_index=True,
        )
    else:
        st.success("No overdue remediation actions.")

    st.subheader("📋 Full Risk Register")
    st.dataframe(
        risks[["risk_id", "title", "category", "business_unit", "likelihood", "impact",
               "inherent_risk", "control_effectiveness", "residual_risk", "owner", "status", "framework_refs"]]
        .sort_values("residual_risk", ascending=False),
        use_container_width=True, hide_index=True,
    )


if __name__ == "__main__":
    main()
