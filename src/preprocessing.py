import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

NUMERICAL_FEATURES = [
    "age", "year", "cgpa", "attendance", "backlogs",
    "internships", "projects", "certifications", "coding_problems",
    "communication_score", "aptitude_score"
]

CATEGORICAL_FEATURES = ["gender", "branch"]

SKILL_FEATURES = [
    "python", "sql", "java", "dsa",
    "machine_learning", "power_bi", "excel"
]

ALL_INPUT_FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES + SKILL_FEATURES
TARGET_COLUMN = "placement"

def build_preprocessor():
    """
    Constructs a ColumnTransformer for preprocessing input features.
    - Numerical features -> StandardScaler
    - Categorical features -> OneHotEncoder(drop='first', handle_unknown='ignore')
    - Skill binary features -> passthrough
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERICAL_FEATURES),
            ("cat", OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("skills", "passthrough", SKILL_FEATURES)
        ],
        remainder="drop"
    )
    return preprocessor

def get_feature_names(preprocessor, categorical_features=CATEGORICAL_FEATURES):
    """
    Retrieves human-readable feature names post ColumnTransformer encoding.
    """
    output_features = list(NUMERICAL_FEATURES)
    
    cat_encoder = preprocessor.named_transformers_["cat"]
    if hasattr(cat_encoder, "get_feature_names_out"):
        encoded_cats = list(cat_encoder.get_feature_names_out(categorical_features))
        output_features.extend(encoded_cats)
    else:
        output_features.extend(categorical_features)
        
    output_features.extend(SKILL_FEATURES)
    return output_features
