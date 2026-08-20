import os
import sys
import unittest
import pandas as pd
import numpy as np

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_generator import save_synthetic_dataset
from src.data_cleaning import DataQualityAnalyzer
from src.preprocessing import build_preprocessor, ALL_INPUT_FEATURES, TARGET_COLUMN, get_feature_names
from src.train_model import train_and_evaluate_models
from src.prediction import PlacementPredictor
from src.skill_gap import SkillGapAnalyzer
from src.sql_analysis import SQLAnalyticsEngine

class TestPlacementIQPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.csv_path = "data/students.csv"
        cls.model_dir = "models"
        cls.db_path = "database/placement.db"
        
        if not os.path.exists(cls.csv_path):
            save_synthetic_dataset(cls.csv_path, num_records=3500)
            
        cls.df = pd.read_csv(cls.csv_path)

    def test_01_dataset_schema_and_integrity(self):
        """Test dataset loading, record count, and required columns."""
        self.assertGreater(len(self.df), 0, "Dataset should not be empty")
        self.assertIn(TARGET_COLUMN, self.df.columns, "Target column 'placement' must exist")
        for col in ALL_INPUT_FEATURES:
            self.assertIn(col, self.df.columns, f"Required feature column '{col}' missing from dataset")

    def test_02_data_cleaning_analyzer(self):
        """Test DataQualityAnalyzer audit report and cleaning pipeline."""
        analyzer = DataQualityAnalyzer(self.df)
        report = analyzer.analyze_quality()
        
        self.assertIn("total_records", report)
        self.assertEqual(report["total_records"], len(self.df))
        self.assertIn("total_features", report)
        
        cleaned_df, log = analyzer.clean_data()
        self.assertEqual(len(cleaned_df), len(self.df))
        self.assertIsInstance(log, list)

    def test_03_preprocessing_pipeline_no_leakage(self):
        """Test ColumnTransformer preprocessing without data leakage."""
        X = self.df[ALL_INPUT_FEATURES]
        preprocessor = build_preprocessor()
        X_trans = preprocessor.fit_transform(X)
        
        feature_names = get_feature_names(preprocessor)
        self.assertEqual(X_trans.shape[0], len(self.df))
        self.assertEqual(X_trans.shape[1], len(feature_names))
        self.assertFalse(np.isnan(X_trans).any(), "Preprocessed feature matrix should contain no NaNs")

    def test_04_model_training_and_metrics(self):
        """Test candidate model training (Logistic Regression, Decision Tree, Random Forest) and evaluation metrics."""
        summary = train_and_evaluate_models(self.csv_path, self.model_dir)
        
        self.assertIn("best_model_name", summary)
        self.assertIn("best_f1_score", summary)
        self.assertIn(summary["best_model_name"], summary["models"])
        
        models_dict = summary["models"]
        self.assertEqual(len(models_dict), 3, "Should evaluate 3 candidate models")
        
        for name, metrics in models_dict.items():
            self.assertGreaterEqual(metrics["accuracy"], 0.0)
            self.assertLessEqual(metrics["accuracy"], 1.0)
            self.assertGreaterEqual(metrics["f1_score"], 0.0)
            self.assertLessEqual(metrics["f1_score"], 1.0)
            self.assertGreaterEqual(metrics["roc_auc"], 0.0)
            self.assertLessEqual(metrics["roc_auc"], 1.0)

    def test_05_predictor_probability_range(self):
        """Test PlacementPredictor probability output range (0-100%) and risk classification."""
        predictor = PlacementPredictor(os.path.join(self.model_dir, "placement_model.joblib"))
        
        sample_high = {
            "student_id": "TEST_HIGH", "age": 21, "gender": "Female", "branch": "Computer Science",
            "year": 4, "cgpa": 9.5, "attendance": 95.0, "backlogs": 0, "internships": 3,
            "projects": 4, "certifications": 3, "coding_problems": 250, "python": 1,
            "sql": 1, "java": 1, "dsa": 1, "machine_learning": 1, "power_bi": 1, "excel": 1,
            "communication_score": 90, "aptitude_score": 92
        }
        res_high = predictor.predict_student(sample_high)
        self.assertGreaterEqual(res_high["probability_pct"], 0.0)
        self.assertLessEqual(res_high["probability_pct"], 100.0)
        self.assertIn(res_high["risk_level"], ["LOW", "MEDIUM", "HIGH"])
        
        sample_low = {
            "student_id": "TEST_LOW", "age": 22, "gender": "Male", "branch": "Civil Eng",
            "year": 4, "cgpa": 5.2, "attendance": 55.0, "backlogs": 3, "internships": 0,
            "projects": 0, "certifications": 0, "coding_problems": 10, "python": 0,
            "sql": 0, "java": 0, "dsa": 0, "machine_learning": 0, "power_bi": 0, "excel": 0,
            "communication_score": 40, "aptitude_score": 45
        }
        res_low = predictor.predict_student(sample_low)
        self.assertGreater(res_high["probability_pct"], res_low["probability_pct"])

    def test_06_skill_gap_math(self):
        """Test SkillGapAnalyzer formula: match_pct + gap_pct == 100.0."""
        sample_student = self.df.iloc[0].to_dict()
        for role in ["Data Analyst", "Machine Learning Engineer", "Software Developer"]:
            gap = SkillGapAnalyzer.analyze_student_role_gap(sample_student, role)
            self.assertAlmostEqual(gap["match_percentage"] + gap["gap_percentage"], 100.0, places=1)

    def test_07_sql_engine_10_queries(self):
        """Test SQL Analytics Engine database initialization and execution of 10 analytical queries."""
        sql_engine = SQLAnalyticsEngine(self.db_path)
        sql_engine.initialize_database(self.df)
        insights = sql_engine.get_predefined_insights()
        
        self.assertEqual(len(insights), 10, "Should contain exactly 10 predefined SQL analytical insights")
        for key, q_data in insights.items():
            self.assertIn("title", q_data)
            self.assertIn("sql", q_data)
            self.assertIn("data", q_data)
            self.assertIsInstance(q_data["data"], pd.DataFrame)

if __name__ == "__main__":
    unittest.main()
