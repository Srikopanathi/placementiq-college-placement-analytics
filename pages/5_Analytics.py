import streamlit as st

from src.ui_utils import load_application_resources, render_header
from src.eda import (
    get_placement_by_cgpa_range_fig,
    get_placement_by_backlogs_fig,
    get_placement_by_internships_fig,
    get_placement_by_projects_fig,
    get_placement_by_coding_fig,
    get_skill_distribution_and_placement_fig,
    get_correlation_heatmap_fig
)

# Load data resources
df_students, quality_report, cleaning_log, sql_engine, metrics_data = load_application_resources()

# Render Header
render_header(
    title="Analytics Workspace",
    description="Explore multi-dimensional placement trends, statistical relationships, and distributions.",
    breadcrumb_suffix="Analytics"
)

# Global Workspace Filters
st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
st.markdown("#### Global Workspace Filters")
f1, f2, f3 = st.columns(3)
with f1:
    f_branch = st.multiselect("Branch", df_students["branch"].unique(), default=df_students["branch"].unique())
with f2:
    f_year = st.multiselect("Academic Year", df_students["year"].unique(), default=df_students["year"].unique())
with f3:
    f_gender = st.multiselect("Gender", df_students["gender"].unique(), default=df_students["gender"].unique())

filtered_df = df_students[
    (df_students["branch"].isin(f_branch)) &
    (df_students["year"].isin(f_year)) &
    (df_students["gender"].isin(f_gender))
]
st.markdown("</div>", unsafe_allow_html=True)

# Categorized Tabs
tab_acad, tab_exp, tab_tech, tab_corr = st.tabs([
    "Academic Analytics", "Experience Analytics", "Technical Analytics", "Correlations & Distributions"
])

with tab_acad:
    ac1, ac2 = st.columns(2)
    with ac1:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.plotly_chart(get_placement_by_cgpa_range_fig(filtered_df), use_container_width=True)
        st.markdown("<div class='insight-banner'>Students in the 8.0+ CGPA range show significantly higher placement success.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with ac2:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.plotly_chart(get_placement_by_backlogs_fig(filtered_df), use_container_width=True)
        st.markdown("<div class='insight-banner'>Active backlogs drastically decrease placement rates due to screening filters.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_exp:
    ec1, ec2 = st.columns(2)
    with ec1:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.plotly_chart(get_placement_by_internships_fig(filtered_df), use_container_width=True)
        st.markdown("<div class='insight-banner'>Students with internship experience have a higher placement rate in this dataset.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with ec2:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.plotly_chart(get_placement_by_projects_fig(filtered_df), use_container_width=True)
        st.markdown("<div class='insight-banner'>Building 2+ projects correlates strongly with successful technical interviews.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_tech:
    tc1, tc2 = st.columns(2)
    with tc1:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.plotly_chart(get_placement_by_coding_fig(filtered_df), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with tc2:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.plotly_chart(get_skill_distribution_and_placement_fig(filtered_df), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_corr:
    st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
    st.plotly_chart(get_correlation_heatmap_fig(filtered_df), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
