import os
import json
import unittest
import pandas as pd
import numpy as np

from src.data_generator import save_synthetic_dataset
from src.data_cleaning import DataQualityAnalyzer
from src.sql_analysis import SQLAnalyticsEngine
from src.train_model import train_and_evaluate_models
from src.preprocessing import ALL_INPUT_FEATURES, NUMERICAL_FEATURES, CATEGORICAL_FEATURES, SKILL_FEATURES
from src.skill_gap import ROLE_REQUIREMENTS

def run_full_audit():
    print("=" * 60)
    print("PLACEMENTIQ - BACKEND, DATASET & ML AUDIT RUNNER")
    print("=" * 60)
    
    csv_path = "data/students.csv"
    model_dir = "models"
    db_path = "database/placement.db"
    
    # 1. Dataset Verification
    if not os.path.exists(csv_path):
        print("Generating dataset...")
        save_synthetic_dataset(csv_path, num_records=3500)
        
    df = pd.read_csv(csv_path)
    total_records = len(df)
    total_features = len(df.columns)
    placed_count = int(df["placement"].sum())
    unplaced_count = total_records - placed_count
    placement_rate = round((placed_count / total_records) * 100, 2)
    
    analyzer = DataQualityAnalyzer(df)
    quality_report = analyzer.analyze_quality()
    cleaned_df, cleaning_log = analyzer.clean_data()
    
    # 2. SQL Database Initialization & Query Audit
    sql_engine = SQLAnalyticsEngine(db_path)
    sql_engine.initialize_database(cleaned_df)
    sql_insights = sql_engine.get_predefined_insights()
    sql_query_count = len(sql_insights)
    
    # 3. Model Training & Evaluation
    print("Training candidate ML models (Logistic Regression, Decision Tree, Random Forest)...")
    summary = train_and_evaluate_models(csv_path, model_dir)
    
    best_name = summary["best_model_name"]
    best_metrics = summary["models"][best_name]
    
    # 4. Feature Stats
    num_orig_features = len(ALL_INPUT_FEATURES)
    # One-hot encoded: gender (1), branch (5), skills (7), num (11) = 24
    num_final_ml_features = 24
    
    # 5. Run Automated Unit Tests
    print("\nRunning automated validation tests...")
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_pipeline.py")
    runner = unittest.TextTestRunner(verbosity=1)
    test_result = runner.run(suite)
    
    if not test_result.wasSuccessful():
        print("[FAIL] Automated test suite failed!")
        return
    else:
        print("[PASSED] Automated test suite PASSED (100% success)!")
        
    # 6. Generate PROJECT_METRICS.md
    metrics_md_content = f"""# PlacementIQ — Project Metrics

## Dataset
- **Dataset Filename**: `data/students.csv`
- **Total Records**: {total_records:,}
- **Total Raw Features**: {total_features}
- **Placed Count**: {placed_count:,}
- **Not Placed Count**: {unplaced_count:,}
- **Placement Rate**: {placement_rate}%

## Data Quality
- **Missing Values**: {quality_report['total_missing']}
- **Duplicates**: {quality_report['duplicate_records']}
- **Data Integrity Status**: {quality_report['status']}

## Machine Learning
- **Models Compared**: 3 (Logistic Regression, Decision Tree, Random Forest)
- **Best Model Selected**: {best_name}
- **Evaluation Split**: 80% Train / 20% Test (Stratified, `random_state=42`)
- **Primary Metric**: F1 Score

### Best Model Performance ({best_name})
- **Accuracy**: {best_metrics['accuracy']:.4f} ({best_metrics['accuracy']*100:.2f}%)
- **Precision**: {best_metrics['precision']:.4f} ({best_metrics['precision']*100:.2f}%)
- **Recall**: {best_metrics['recall']:.4f} ({best_metrics['recall']*100:.2f}%)
- **F1 Score**: {best_metrics['f1_score']:.4f} ({best_metrics['f1_score']*100:.2f}%)
- **ROC-AUC**: {best_metrics['roc_auc']:.4f}

### Candidate Models Comparison
| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for m_name, m_val in summary["models"].items():
        metrics_md_content += f"| {m_name} | {m_val['accuracy']:.4f} | {m_val['precision']:.4f} | {m_val['recall']:.4f} | {m_val['f1_score']:.4f} | {m_val['roc_auc']:.4f} |\n"

    metrics_md_content += f"""
## Feature Engineering
- **Original Feature Count**: {num_orig_features}
- **Final ML Features**: {num_final_ml_features} (One-Hot Encoded & Scaled)
- **Top 5 Contributing Features**:
"""
    top_5_feats = list(best_metrics["feature_importances"].items())[:5]
    for feat, imp in top_5_feats:
        metrics_md_content += f"  - `{feat}`: {imp:.4f}\n"

    metrics_md_content += f"""
## Analytics & Database
- **SQL Queries Executed**: {sql_query_count}
- **KPI Metrics Tracked**: 5 (Total Students, Placement Rate, Avg CGPA, Avg Coding, High-Risk Count)
- **Career Roles Benchmarked**: 3 (Data Analyst, ML Engineer, Software Developer)

## Application Architecture
- **Navigation Pages**: 9 Independent Pages
- **Routing Engine**: Streamlit Multipage (`st.navigation`, `st.Page`)
- **CSV Export Feature**: Integrated in Placement Officer Desk
"""

    with open("PROJECT_METRICS.md", "w", encoding="utf-8") as f:
        f.write(metrics_md_content)
        
    print("\nSuccessfully updated PROJECT_METRICS.md with empirical metrics.")

    # 7. Print Terminal Output — RESUME-READY METRICS
    print("\n" + "=" * 60)
    print("RESUME-READY METRICS")
    print("=" * 60)
    print(f"""
Dataset:
[{total_records:,}] student records
[{total_features}] features

ML:
[3] models compared (Logistic Regression, Decision Tree, Random Forest)
Best Model: [{best_name}]
Accuracy: [{best_metrics['accuracy']:.4f}]
Precision: [{best_metrics['precision']:.4f}]
Recall: [{best_metrics['recall']:.4f}]
F1: [{best_metrics['f1_score']:.4f}]
ROC-AUC: [{best_metrics['roc_auc']:.4f}]

Analytics:
[{sql_query_count}] SQL queries
[5] KPIs
[{len(ROLE_REQUIREMENTS)}] career roles

Application:
[9] pages
""")
    print("=" * 60)

if __name__ == "__main__":
    run_full_audit()
