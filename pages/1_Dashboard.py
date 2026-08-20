import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from src.ui_utils import load_application_resources, render_header
from src.eda import (
    get_placement_distribution_fig,
    get_placement_by_cgpa_range_fig,
    get_placement_by_internships_fig,
    get_top_skill_gaps_fig
)

# Load data resources
df_students, quality_report, cleaning_log, sql_engine, metrics_data = load_application_resources()

# Render Header
render_header(
    title="Placement Intelligence Dashboard",
    description="Monitor student placement readiness and identify areas requiring intervention.",
    breadcrumb_suffix="Dashboard"
)

# Calculate KPI Metrics
total_students = len(df_students)
placed_count = int(df_students["placement"].sum())
placement_rate = round((placed_count / total_students) * 100, 1)
avg_cgpa = round(df_students["cgpa"].mean(), 2)
avg_coding = round(df_students["coding_problems"].mean(), 1)
high_risk_count = len(df_students[(df_students["cgpa"] < 6.5) & (df_students["backlogs"] > 0)])

# 5 KPI Cards
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""
    <div class='kpi-container'>
        <div class='kpi-label'>Total Students</div>
        <div class='kpi-value'>{total_students:,}</div>
        <div class='kpi-subtext'>Across all branches</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class='kpi-container'>
        <div class='kpi-label'>Placement Rate</div>
        <div class='kpi-value'>{placement_rate}%</div>
        <div class='kpi-subtext'>{placed_count:,} placed</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class='kpi-container'>
        <div class='kpi-label'>Average CGPA</div>
        <div class='kpi-value'>{avg_cgpa}</div>
        <div class='kpi-subtext'>Out of 10.0</div>
    </div>
    """, unsafe_allow_html=True)
with k4:
    st.markdown(f"""
    <div class='kpi-container'>
        <div class='kpi-label'>Avg Coding Problems</div>
        <div class='kpi-value'>{avg_coding}</div>
        <div class='kpi-subtext'>Problems solved</div>
    </div>
    """, unsafe_allow_html=True)
with k5:
    st.markdown(f"""
    <div class='kpi-container'>
        <div class='kpi-label'>High-Risk Students</div>
        <div class='kpi-value' style='color: #DC2626;'>{high_risk_count}</div>
        <div class='kpi-subtext' style='color: #DC2626;'>Requires intervention</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# Section 1: Placement Overview & Placement Readiness Risk Category Distribution
c_overview, c_readiness = st.columns(2)
with c_overview:
    st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
    st.plotly_chart(get_placement_distribution_fig(df_students), use_container_width=True)
    st.markdown(f"<div class='insight-banner'><strong>Dataset Insight:</strong> Overall placement rate stands at {placement_rate}%. Academic performance and practical coding are key drivers.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c_readiness:
    st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
    low_risk = len(df_students[(df_students["cgpa"] >= 7.5) & (df_students["backlogs"] == 0)])
    high_risk = high_risk_count
    med_risk = total_students - low_risk - high_risk
    
    df_risk = pd.DataFrame({
        "Risk Category": ["Low Risk", "Medium Risk", "High Risk"],
        "Student Count": [low_risk, med_risk, high_risk]
    })
    fig_risk = px.bar(
        df_risk,
        x="Risk Category",
        y="Student Count",
        color="Risk Category",
        color_discrete_map={"Low Risk": "#10B981", "Medium Risk": "#F59E0B", "High Risk": "#EF4444"},
        text="Student Count"
    )
    fig_risk.update_layout(
        title="Placement Readiness Risk Category Distribution",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#475569"),
        margin=dict(l=20, r=20, t=50, b=40),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9")
    )
    fig_risk.update_traces(textposition='outside')
    st.plotly_chart(fig_risk, use_container_width=True)
    st.markdown("<div class='insight-banner'><strong>Placement Readiness:</strong> High-risk students are defined by CGPA &lt; 6.5 and active backlogs.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Section 2: Analytics Grid (CGPA & Internships)
col_cgpa, col_intern = st.columns(2)
with col_cgpa:
    st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
    st.plotly_chart(get_placement_by_cgpa_range_fig(df_students), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
with col_intern:
    st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
    st.plotly_chart(get_placement_by_internships_fig(df_students), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Section 3: Skill Insights
col_gap, col_val = st.columns(2)
with col_gap:
    st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
    st.plotly_chart(get_top_skill_gaps_fig(df_students), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_val:
    st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
    st.markdown("### Most Valuable Technical Skills")
    st.caption("Skills strongly associated with higher placement rates in this dataset:")
    
    skills = ["python", "sql", "java", "dsa", "machine_learning", "power_bi", "excel"]
    skill_rates = []
    for s in skills:
        r = df_students[df_students[s] == 1]["placement"].mean() * 100
        skill_rates.append({"Skill": s.upper().replace("_", " "), "Placement Rate (%)": round(r, 1)})
    df_val_skills = pd.DataFrame(skill_rates).sort_values(by="Placement Rate (%)", ascending=False)
    
    for idx, row in df_val_skills.iterrows():
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between; align-items: center; padding: 10px 12px; border-bottom: 1px solid #F1F5F9;'>
            <span style='font-weight: 600; color: #0F172A;'>{row['Skill']}</span>
            <span style='font-weight: 700; color: #059669;'>{row['Placement Rate (%)']}% Placement Rate</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Section 4: Students Requiring Attention Table
st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
st.markdown("### Students Requiring Attention")
st.caption("Students identified with active backlogs or low CGPA requiring placement cell support:")

df_attention = df_students[(df_students["cgpa"] < 6.5) | (df_students["backlogs"] > 0)].copy()
df_attention["Risk"] = np.where(df_attention["cgpa"] < 6.0, "HIGH", "MEDIUM")
df_attention["Top Skill Gap"] = np.where(df_attention["dsa"] == 0, "DSA", np.where(df_attention["sql"] == 0, "SQL", "Projects"))

display_df = df_attention[["student_id", "branch", "cgpa", "backlogs", "internships", "Risk", "Top Skill Gap"]].head(10)
st.dataframe(display_df, use_container_width=True)

if st.button("View Student Analysis Desk"):
    st.switch_page("pages/2_Student_Analysis.py")
st.markdown("</div>", unsafe_allow_html=True)
