import streamlit as st

from src.ui_utils import load_application_resources, render_header

# Load data & SQL engine
df_students, quality_report, cleaning_log, sql_engine, metrics_data = load_application_resources()

# Render Header
render_header(
    title="Placement Officer Insights",
    description="Administrative intelligence desk for identifying students requiring targeted support.",
    breadcrumb_suffix="Placement Officer"
)

insights = sql_engine.get_predefined_insights()

# Executive KPI Cards for Placement Officer
high_risk_num = len(df_students[(df_students["cgpa"] < 6.5) & (df_students["backlogs"] > 0)])
med_risk_num = len(df_students[(df_students["cgpa"] >= 6.5) & (df_students["cgpa"] < 7.5)])
placed_pct = round((df_students["placement"].sum() / len(df_students)) * 100, 1)
gapped_num = len(df_students[df_students["dsa"] == 0])

ok1, ok2, ok3, ok4 = st.columns(4)
ok1.metric("High-Risk Students", high_risk_num)
ok2.metric("Medium-Risk Students", med_risk_num)
ok3.metric("Placement Rate", f"{placed_pct}%")
ok4.metric("DSA Skill Gaps", gapped_num)

st.markdown("<br/>", unsafe_allow_html=True)

st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
st.markdown("### Student Intervention Workspace")

officer_view = st.selectbox(
    "Select Administrative Filter",
    [
        "High Risk Students (Low CGPA & Active Backlogs)",
        "High Academic Performers (CGPA >= 8.0) Missing Internships",
        "Strong Coders (>= 150 problems) Weak Communication",
        "Branch Placement Summary"
    ]
)

if "High Risk" in officer_view:
    data_table = insights["high_risk_students"]["data"]
elif "High Academic" in officer_view:
    data_table = insights["high_cgpa_no_internship"]["data"]
elif "Strong Coders" in officer_view:
    data_table = insights["strong_coder_weak_comm"]["data"]
else:
    data_table = insights["placement_by_branch"]["data"]

st.dataframe(data_table, use_container_width=True)

csv_data = data_table.to_csv(index=False).encode('utf-8')
st.download_button("📥 Export CSV Report", csv_data, "placement_officer_report.csv", "text/csv")
st.markdown("</div>", unsafe_allow_html=True)
