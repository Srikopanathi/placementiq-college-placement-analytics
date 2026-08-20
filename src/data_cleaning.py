import pandas as pd
import numpy as np

class DataQualityAnalyzer:
    """
    Performs data quality checks, validation, missing value handling,
    and returns a structured data quality audit report.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.raw_count = len(df)
        self.raw_cols = list(df.columns)
        
    def analyze_quality(self):
        """
        Runs comprehensive audit checks on the dataset.
        """
        # Missing values check
        missing_series = self.df.isnull().sum()
        total_missing = int(missing_series.sum())
        missing_by_col = missing_series[missing_series > 0].to_dict()
        
        # Duplicate records check
        duplicate_count = int(self.df.duplicated(subset=["student_id"]).sum())
        
        # Data types validation
        num_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = self.df.select_dtypes(include=["object", "category"]).columns.tolist()
        
        # Numerical range validation checks
        invalid_ranges = {}
        range_rules = {
            "cgpa": (0.0, 10.0),
            "attendance": (0.0, 100.0),
            "backlogs": (0, 20),
            "communication_score": (0.0, 100.0),
            "aptitude_score": (0.0, 100.0),
            "age": (15, 60),
            "coding_problems": (0, 5000),
            "internships": (0, 20),
            "projects": (0, 30),
            "certifications": (0, 50)
        }
        
        for col, (min_val, max_val) in range_rules.items():
            if col in self.df.columns:
                out_of_bounds = self.df[(self.df[col] < min_val) | (self.df[col] > max_val)]
                if len(out_of_bounds) > 0:
                    invalid_ranges[col] = len(out_of_bounds)
                    
        # Outlier detection using IQR method for numerical columns
        outlier_counts = {}
        for col in ["cgpa", "attendance", "coding_problems", "communication_score", "aptitude_score"]:
            if col in self.df.columns:
                q1 = self.df[col].quantile(0.25)
                q3 = self.df[col].quantile(0.75)
                iqr = q3 - q1
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
                outliers = self.df[(self.df[col] < lower) | (self.df[col] > upper)]
                outlier_counts[col] = len(outliers)
                
        status = "PASSED (Clean)" if (total_missing == 0 and duplicate_count == 0 and len(invalid_ranges) == 0) else "ISSUES DETECTED"
        
        report = {
            "total_records": self.raw_count,
            "total_features": len(self.raw_cols),
            "total_missing": total_missing,
            "missing_by_col": missing_by_col,
            "duplicate_records": duplicate_count,
            "numerical_columns": len(num_cols),
            "categorical_columns": len(cat_cols),
            "invalid_range_counts": invalid_ranges,
            "outlier_counts": outlier_counts,
            "status": status,
            "cleaned_records": self.raw_count - duplicate_count
        }
        
        return report

    def clean_data(self):
        """
        Cleans dataset by dropping duplicates and imputing missing values if present.
        Returns cleaned DataFrame and cleaning log.
        """
        cleaned_df = self.df.copy()
        log = []
        
        # Remove duplicate student IDs
        dups = cleaned_df.duplicated(subset=["student_id"]).sum()
        if dups > 0:
            cleaned_df = cleaned_df.drop_duplicates(subset=["student_id"]).reset_index(drop=True)
            log.append(f"Removed {dups} duplicate student_id records.")
            
        # Missing values handling
        for col in cleaned_df.columns:
            if cleaned_df[col].isnull().sum() > 0:
                if cleaned_df[col].dtype in [np.float64, np.int64]:
                    median_val = cleaned_df[col].median()
                    cleaned_df[col].fillna(median_val, inplace=True)
                    log.append(f"Imputed missing numerical values in '{col}' with median {median_val}.")
                else:
                    mode_val = cleaned_df[col].mode()[0]
                    cleaned_df[col].fillna(mode_val, inplace=True)
                    log.append(f"Imputed missing categorical values in '{col}' with mode '{mode_val}'.")
                    
        # Numerical range clipping sanity
        range_rules = {
            "cgpa": (0.0, 10.0),
            "attendance": (0.0, 100.0),
            "communication_score": (0.0, 100.0),
            "aptitude_score": (0.0, 100.0)
        }
        for col, (min_v, max_v) in range_rules.items():
            if col in cleaned_df.columns:
                cleaned_df[col] = cleaned_df[col].clip(min_v, max_v)
                
        return cleaned_df, log
