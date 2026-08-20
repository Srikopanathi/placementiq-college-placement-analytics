import streamlit as st

from src.ui_utils import load_application_resources, render_header
from src.skill_gap import SkillGapAnalyzer

# Load data resources
df_students, quality_report, cleaning_log, sql_engine, metrics_data = load_application_resources()

# Render Header
render_header(
    title="Skill Gap Analyzer",
    description="Compare student capabilities with target career role requirements.",
    breadcrumb_suffix="Skill Gap Analyzer"
)

# Selectors Card
st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
c_s1, c_s2 = st.columns(2)
with c_s1:
    sel_stu = st.selectbox("Select Student", df_students["student_id"].tolist())
with c_s2:
    sel_role = st.selectbox("Target Career Role", ["Data Analyst", "Machine Learning Engineer", "Software Developer"])
st.markdown("</div>", unsafe_allow_html=True)

stu_data = df_students[df_students["student_id"] == sel_stu].iloc[0].to_dict()
gap_info = SkillGapAnalyzer.analyze_student_role_gap(stu_data, sel_role)

# Benchmark Card
st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
st.markdown(f"### Role Readiness Benchmark: {sel_role}")

gm1, gm2 = st.columns(2)
gm1.metric("Skill Match Score", f"{gap_info['match_percentage']}%")
gm2.metric("Skill Gap Percentage", f"{gap_info['gap_percentage']}%")

st.progress(gap_info['match_percentage'] / 100.0)

mc1, mc2 = st.columns(2)
with mc1:
    st.markdown("#### Matched Skills")
    if gap_info["matching_skills"]:
        for m in gap_info["matching_skills"]:
            st.markdown(f"- ✔️ <span style='color:#059669; font-weight:600;'>{m}</span>", unsafe_allow_html=True)
    else:
        st.caption("No matched benchmark skills identified.")

with mc2:
    st.markdown("#### Missing Skills")
    if gap_info["missing_skills"]:
        for mis in gap_info["missing_skills"]:
            p_color = "#DC2626" if mis["priority"] == "High" else "#D97706"
            st.markdown(f"- ✕ <span style='color:{p_color}; font-weight:600;'>[{mis['priority']}] {mis['skill']}</span>", unsafe_allow_html=True)
    else:
        st.success("All role requirements met!")

st.markdown("</div>", unsafe_allow_html=True)
