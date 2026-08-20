import os
import json
import pandas as pd
import streamlit as st

from src.data_generator import save_synthetic_dataset
from src.data_cleaning import DataQualityAnalyzer
from src.sql_analysis import SQLAnalyticsEngine
from src.train_model import train_and_evaluate_models
from src.prediction import PlacementPredictor

@st.cache_data
def load_application_resources():
    csv_path = "data/students.csv"
    db_path = "database/placement.db"
    model_path = "models/placement_model.joblib"
    metrics_path = "models/model_metrics.json"

    if not os.path.exists(csv_path):
        save_synthetic_dataset(csv_path, num_records=3500)

    df = pd.read_csv(csv_path)

    analyzer = DataQualityAnalyzer(df)
    quality_report = analyzer.analyze_quality()
    cleaned_df, cleaning_log = analyzer.clean_data()

    sql_engine = SQLAnalyticsEngine(db_path)
    sql_engine.initialize_database(cleaned_df)

    if not os.path.exists(model_path) or not os.path.exists(metrics_path):
        train_and_evaluate_models(csv_path, "models")

    with open(metrics_path, "r") as f:
        metrics_data = json.load(f)

    return cleaned_df, quality_report, cleaning_log, sql_engine, metrics_data

@st.cache_resource
def get_predictor():
    return PlacementPredictor("models/placement_model.joblib")

def load_css():
    st.markdown("""
    <style>
        /* Global Base Styling */
        .stApp {
            background-color: #F8FAFC;
            color: #0F172A;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }

        /* Top Breadcrumb & Page Header */
        .breadcrumb {
            font-size: 0.85rem;
            font-weight: 600;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }
        .page-header-title {
            font-size: 1.85rem;
            font-weight: 800;
            color: #0F172A;
            letter-spacing: -0.02em;
            margin-bottom: 4px;
        }
        .page-header-desc {
            font-size: 0.95rem;
            color: #475569;
            margin-bottom: 24px;
        }

        /* SaaS Card Design */
        .saas-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04), 0 1px 2px -1px rgba(0, 0, 0, 0.04);
            margin-bottom: 16px;
        }
        
        /* SaaS KPI Card */
        .kpi-container {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 18px 20px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
        }
        .kpi-label {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #64748B;
            margin-bottom: 6px;
        }
        .kpi-value {
            font-size: 1.75rem;
            font-weight: 800;
            color: #0F172A;
            line-height: 1.2;
        }
        .kpi-subtext {
            font-size: 0.8rem;
            color: #2563EB;
            font-weight: 500;
            margin-top: 6px;
        }

        /* Status & Risk Badges */
        .badge-risk-low {
            background-color: #ECFDF5;
            color: #047857;
            border: 1px solid #A7F3D0;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 700;
            display: inline-block;
        }
        .badge-risk-medium {
            background-color: #FFFBEB;
            color: #B45309;
            border: 1px solid #FDE68A;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 700;
            display: inline-block;
        }
        .badge-risk-high {
            background-color: #FEF2F2;
            color: #B91C1C;
            border: 1px solid #FECACA;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 700;
            display: inline-block;
        }
        
        /* Skill Badges */
        .skill-badge-verified {
            background-color: #EFF6FF;
            color: #1D4ED8;
            border: 1px solid #BFDBFE;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
            margin-right: 6px;
            margin-bottom: 6px;
        }
        .skill-badge-missing {
            background-color: #F8FAFC;
            color: #94A3B8;
            border: 1px solid #E2E8F0;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 500;
            display: inline-block;
            margin-right: 6px;
            margin-bottom: 6px;
        }

        /* Insight Banner */
        .insight-banner {
            background-color: #F8FAFC;
            border-left: 4px solid #2563EB;
            padding: 10px 14px;
            font-size: 0.85rem;
            color: #334155;
            border-radius: 0 6px 6px 0;
            margin-top: 8px;
        }

        /* Primary Button Styling */
        .stButton > button {
            background-color: #2563EB !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            border: none !important;
            padding: 8px 16px !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        }
        .stButton > button:hover {
            background-color: #1D4ED8 !important;
        }

        /* Sidebar Clean Styling */
        [data-testid="stSidebar"] {
            background-color: #0F172A;
            color: #F8FAFC;
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #CBD5E1;
        }
        [data-testid="stSidebarNav"] span {
            color: #CBD5E1 !important;
            font-size: 0.95rem !important;
            font-weight: 500 !important;
        }
        [data-testid="stSidebarNav"] a:hover span {
            color: #FFFFFF !important;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background-color: #1E293B !important;
            border-left: 4px solid #2563EB !important;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] span {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_header(title: str, description: str, breadcrumb_suffix: str):
    st.markdown(f"<div class='breadcrumb'>PlacementIQ &nbsp;/&nbsp; {breadcrumb_suffix}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='page-header-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='page-header-desc'>{description}</div>", unsafe_allow_html=True)

def render_sidebar_header():
    st.sidebar.markdown("""
    <div style='padding: 5px 0px 10px 0px;'>
        <div style='font-size: 1.4rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;'>
            PLACEMENTIQ
        </div>
        <div style='font-size: 0.78rem; color: #94A3B8; font-weight: 500;'>
            College Placement Intelligence
        </div>
    </div>
    <hr style='border-color: #334155; margin: 8px 0px 12px 0px;'/>
    """, unsafe_allow_html=True)

def render_sidebar_footer():
    st.sidebar.markdown("""
    <hr style='border-color: #334155; margin: 15px 0px 10px 0px;'/>
    <div style='font-size: 0.8rem; color: #CBD5E1; line-height: 1.6;'>
        <div style='margin-bottom: 2px;'><strong>Data Status</strong></div>
        <div style='color: #10B981; font-weight: 600; margin-bottom: 8px;'>● Connected</div>
        <div style='margin-bottom: 2px;'><strong>Model Status</strong></div>
        <div style='color: #10B981; font-weight: 600;'>● Ready</div>
    </div>
    """, unsafe_allow_html=True)
