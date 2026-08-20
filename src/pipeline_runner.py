import sys
import os
sys.path.insert(0, os.path.abspath("."))

from src.data_generator import save_synthetic_dataset
from src.data_cleaning import DataQualityAnalyzer
from src.sql_analysis import SQLAnalyticsEngine
from src.train_model import train_and_evaluate_models

def run_pipeline():
    print("--- Step 1: Generating Dataset ---")
    df = save_synthetic_dataset("data/students.csv", num_records=3500)

    print("--- Step 2: Quality Analysis & Cleaning ---")
    analyzer = DataQualityAnalyzer(df)
    report = analyzer.analyze_quality()
    cleaned_df, log = analyzer.clean_data()
    print("Data Quality Status:", report["status"])

    print("--- Step 3: SQLite DB Initialization ---")
    sql_engine = SQLAnalyticsEngine("database/placement.db")
    sql_engine.initialize_database(cleaned_df)
    print("Database initialized with", len(cleaned_df), "records.")

    print("--- Step 4: ML Pipeline Training & Evaluation ---")
    summary = train_and_evaluate_models("data/students.csv", "models")
    print(f"ML Training Complete. Best Model: {summary['best_model_name']} | Best F1: {summary['best_f1_score']}")

if __name__ == "__main__":
    run_pipeline()
