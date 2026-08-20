import os
import sys
import streamlit as st

# Add current path for local imports
sys.path.insert(0, os.path.abspath("."))

from src.ui_utils import load_css, render_sidebar_header, render_sidebar_footer

# ----------------------------------------------------
# STREAMLIT PAGE CONFIGURATION
# ----------------------------------------------------
st.set_page_config(
    page_title="PlacementIQ - College Placement Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load global CSS styling
load_css()

# Render Sidebar Branding (Header)
render_sidebar_header()

# Define Multipage Navigation with 9 Independent Pages
pages = [
    st.Page("pages/1_Dashboard.py", title="Dashboard", icon="🏠", default=True),
    st.Page("pages/2_Student_Analysis.py", title="Student Analysis", icon="👨‍🎓"),
    st.Page("pages/3_Placement_Prediction.py", title="Placement Prediction", icon="🎯"),
    st.Page("pages/4_Skill_Gap_Analyzer.py", title="Skill Gap Analyzer", icon="🧩"),
    st.Page("pages/5_Analytics.py", title="Analytics", icon="📊"),
    st.Page("pages/6_Model_Performance.py", title="Model Performance", icon="🤖"),
    st.Page("pages/7_Placement_Officer.py", title="Placement Officer", icon="👔"),
    st.Page("pages/8_Data_Quality.py", title="Data Quality", icon="📋"),
    st.Page("pages/9_About.py", title="About", icon="ℹ️"),
]

# Initialize Streamlit Navigation
pg = st.navigation(pages)

# Render Sidebar Footer (Status)
render_sidebar_footer()

# Run current selected independent page
pg.run()

# ----------------------------------------------------
# VERCEL DEPLOYMENT COMPATIBILITY
# ----------------------------------------------------
def handler(request=None, response=None):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": "<h1>PlacementIQ Analytics</h1><p>Running Streamlit Engine</p>"
    }

app = handler
application = handler

