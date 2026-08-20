import streamlit as st

from src.ui_utils import load_application_resources, get_predictor, render_header

# Load predictor
predictor = get_predictor()

# Render Header
render_header(
    title="Placement Prediction",
    description="Estimate student placement probability using the trained classification model.",
    breadcrumb_suffix="Placement Prediction"
)

# Interactive Prediction Form
with st.form("pred_form_saas"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.markdown("#### Academic Profile")
        in_cgpa = st.slider("CGPA", 5.0, 10.0, 7.8, 0.1)
        in_attendance = st.slider("Attendance (%)", 50.0, 100.0, 80.0, 1.0)
        in_backlogs = st.number_input("Active Backlogs", 0, 5, 0)
        in_branch = st.selectbox("Branch", ["Computer Science", "Information Technology", "Electronics & Comm", "Electrical Eng", "Mechanical Eng", "Civil Eng"])
        in_year = st.selectbox("Academic Year", [3, 4], index=1)
        in_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        in_age = st.number_input("Age", 18, 30, 21)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.markdown("#### Soft Skills")
        in_comm = st.slider("Communication Score (0-100)", 0, 100, 70)
        in_apt = st.slider("Aptitude Score (0-100)", 0, 100, 72)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.markdown("#### Experience & Practice")
        in_internships = st.number_input("Internships", 0, 4, 1)
        in_projects = st.number_input("Projects Completed", 0, 6, 2)
        in_certifications = st.number_input("Certifications", 0, 10, 2)
        in_coding = st.number_input("Coding Problems Solved", 0, 300, 120)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.markdown("#### Technical Preparation")
        sp_py = st.checkbox("Python", value=True)
        sp_sql = st.checkbox("SQL", value=True)
        sp_java = st.checkbox("Java", value=False)
        sp_dsa = st.checkbox("DSA", value=True)
        sp_ml = st.checkbox("Machine Learning", value=False)
        sp_pbi = st.checkbox("Power BI", value=False)
        sp_excel = st.checkbox("Excel", value=True)
        st.markdown("</div>", unsafe_allow_html=True)

    submit_pred = st.form_submit_button("Analyze Placement Readiness", use_container_width=True)

if submit_pred:
    custom_input = {
        "student_id": "CUSTOM",
        "age": in_age,
        "gender": in_gender,
        "branch": in_branch,
        "year": in_year,
        "cgpa": in_cgpa,
        "attendance": in_attendance,
        "backlogs": in_backlogs,
        "internships": in_internships,
        "projects": in_projects,
        "certifications": in_certifications,
        "coding_problems": in_coding,
        "python": int(sp_py),
        "sql": int(sp_sql),
        "java": int(sp_java),
        "dsa": int(sp_dsa),
        "machine_learning": int(sp_ml),
        "power_bi": int(sp_pbi),
        "excel": int(sp_excel),
        "communication_score": in_comm,
        "aptitude_score": in_apt
    }

    res = predictor.predict_student(custom_input)

    st.markdown("<div class='saas-card' style='border-top: 4px solid #2563EB;'>", unsafe_allow_html=True)
    st.markdown("### Prediction Results")
    rc1, rc2, rc3 = st.columns(3)
    rc1.metric("Placement Probability", f"{res['probability_pct']}%")
    rc2.metric("Predicted Status", res["status"])
    
    r_cls = f"badge-risk-{res['risk_level'].lower()}"
    rc3.markdown(f"<div class='kpi-label'>Risk Level</div><div style='margin-top:8px;'><span class='{r_cls}'>{res['risk_level']} RISK</span></div>", unsafe_allow_html=True)

    st.markdown("#### Key Contributing Factors")
    for desc, f_type in res["contributing_factors"]:
        icon = "✔️" if f_type == "Positive" else "⚠️"
        color = "#059669" if f_type == "Positive" else "#DC2626"
        st.markdown(f"- {icon} <span style='color: {color}; font-weight: 600;'>[{f_type}]</span> {desc}", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
