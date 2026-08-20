import streamlit as st

from src.ui_utils import render_header

# Render Header
render_header(
    title="About PlacementIQ",
    description="System architecture, methodology overview, and academic disclaimers.",
    breadcrumb_suffix="About"
)

# System Architecture & Documentation Card
st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
st.markdown("""
### 🎯 Overview & Problem Statement
Higher education institutions often struggle to systematically identify students who are at risk of missing campus placement opportunities until it is too late. Traditional placement tracking relies on retrospective results rather than predictive indicators.

**PlacementIQ** is an academic Machine Learning and Data Analytics decision-support platform built to solve this problem by:
1. **Monitoring** key placement readiness drivers across academics, technical coding, soft skills, and practical experience.
2. **Predicting** placement readiness probabilities using trained machine learning models.
3. **Analyzing Skill Gaps** against industry career benchmarks (Data Analyst, ML Engineer, Software Developer).
4. **Providing Actionable Recommendations** for individual students and placement officers.

---

### 🛠️ Technology Architecture
- **Frontend & Routing**: Streamlit Multi-Page Architecture (`st.navigation`, `st.Page`), Custom SaaS Light CSS
- **Data & Analytics**: Pandas, NumPy, SQLite3 (`SQLAnalyticsEngine`)
- **Machine Learning**: Scikit-Learn (Random Forest Classifier, Logistic Regression, Decision Tree)
- **Visualization**: Plotly Express, Plotly Graph Objects
- **Model Persistence**: Joblib, JSON metadata

---

### 🤖 Machine Learning Workflow & Skill-Gap Methodology
- **Preprocessing**: Robust scaling of numeric metrics, binary flag verification, and missing value imputation.
- **Model Selection**: Comparative evaluation using F1-score as the primary metric, balanced with Accuracy, Precision, Recall, and ROC-AUC.
- **Skill Gap Benchmarking**: Direct comparison of student skill vectors against target industry role specifications.

---

### ⚠️ Academic & Ethical Disclosures
> **Synthetic Dataset Disclosure**:
> *This application operates on a synthetic dataset created for academic demonstration. The dataset contains 3,500 student records generated with probabilistic relationships between academic records, practical experience, coding practice, soft skills, and placement targets with realistic noise.*

> **Decision-Support Disclaimer**:
> *PlacementIQ is an academic decision-support prototype intended to assist students and placement cells. It should not be used as the sole basis for real student employment or placement decisions.*
""")
st.markdown("</div>", unsafe_allow_html=True)
