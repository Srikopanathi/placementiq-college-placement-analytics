import streamlit as st
import pandas as pd

from src.ui_utils import load_application_resources, get_predictor, render_header
from src.recommendations import RecommendationEngine

# Load data resources & predictor
df_students, quality_report, cleaning_log, sql_engine, metrics_data = load_application_resources()
predictor = get_predictor()

# Render Header
render_header(
    title="Student Analysis",
    description="Explore individual student placement readiness, skill matrices, and dynamic improvement recommendations.",
    breadcrumb_suffix="Student Analysis"
)

# Student Selector
st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
selected_student_id = st.selectbox(
    "Search or Select Student ID",
    options=df_students["student_id"].tolist(),
    index=0
)
st.markdown("</div>", unsafe_allow_html=True)

student_row = df_students[df_students["student_id"] == selected_student_id].iloc[0].to_dict()
pred_res = predictor.predict_student(student_row)

# Profile Banner Header
st.markdown(f"""
<div class='saas-card' style='background: linear-gradient(90deg, #1E3A8A 0%, #2563EB 100%); color: #FFFFFF;'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <h2 style='color: #FFFFFF; margin: 0;'>Student ID: {student_row['student_id']}</h2>
            <div style='color: #93C5FD; font-size: 0.95rem; margin-top: 4px;'>
                {student_row['branch']} &nbsp;|&nbsp; Year {student_row['year']} &nbsp;|&nbsp; Age {student_row['age']}
            </div>
        </div>
        <div style='text-align: right;'>
            <div style='font-size: 0.8rem; color: #93C5FD; text-transform: uppercase;'>Actual Outcome</div>
            <div style='font-size: 1.2rem; font-weight: 800; color: #FFFFFF;'>
                {"PLACED" if student_row["placement"] == 1 else "NOT PLACED"}
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Academic KPIs & Prediction Card
col_prof, col_pred = st.columns([3, 2])
with col_prof:
    st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
    st.markdown("### Academic & Experience Metrics")
    pk1, pk2, pk3, pk4 = st.columns(4)
    pk1.metric("CGPA", f"{student_row['cgpa']} / 10")
    pk2.metric("Attendance", f"{student_row['attendance']}%")
    pk3.metric("Backlogs", f"{student_row['backlogs']}")
    pk4.metric("Internships", f"{student_row['internships']}")
    
    st.divider()
    pk5, pk6, pk7, pk8 = st.columns(4)
    pk5.metric("Projects", f"{student_row['projects']}")
    pk6.metric("Coding Solved", f"{student_row['coding_problems']}")
    pk7.metric("Comm Score", f"{student_row['communication_score']}")
    pk8.metric("Aptitude Score", f"{student_row['aptitude_score']}")
    st.markdown("</div>", unsafe_allow_html=True)

with col_pred:
    st.markdown("<div class='saas-card' style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<div class='kpi-label'>Placement Readiness</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 2.5rem; font-weight: 800; color: #2563EB;'>{pred_res['probability_pct']}%</div>", unsafe_allow_html=True)
    
    risk_cls = f"badge-risk-{pred_res['risk_level'].lower()}"
    st.markdown(f"<div style='margin-top: 10px;'><span class='{risk_cls}'>{pred_res['risk_level']} RISK</span> &nbsp;|&nbsp; <strong>{pred_res['status']}</strong></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Skill Profile & Verification
st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
st.markdown("### Skill Profile & Verification")

verified_badges = ""
for s in ["python", "sql", "java", "dsa", "machine_learning", "power_bi", "excel"]:
    s_name = s.upper().replace("_", " ")
    if student_row.get(s, 0) == 1:
        verified_badges += f"<span class='skill-badge-verified'>✓ {s_name}</span>"
    else:
        verified_badges += f"<span class='skill-badge-missing'>✕ {s_name}</span>"
st.markdown(verified_badges, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Recommendations Panel
st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
st.markdown("### Recommended Actions")
target_role_select = st.selectbox("Target Career Role Benchmark", ["Data Analyst", "Machine Learning Engineer", "Software Developer"])
recs = RecommendationEngine.generate_recommendations(student_row, target_role_select)

for r in recs:
    p_color = "#DC2626" if r["priority"] == "HIGH" else "#D97706"
    st.markdown(f"""
    <div style='background-color: #F8FAFC; border-left: 4px solid {p_color}; padding: 12px 16px; margin-bottom: 10px; border-radius: 4px;'>
        <div style='font-weight: 700; color: {p_color};'>[{r['priority']} PRIORITY] {r['skill']}</div>
        <div style='color: #475569; font-size: 0.9rem; margin-top: 2px;'><strong>Reason:</strong> {r['reason']}</div>
        <div style='color: #2563EB; font-size: 0.9rem; margin-top: 2px;'><strong>Action:</strong> {r['action']}</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
