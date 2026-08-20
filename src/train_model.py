import os
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve
)

from src.preprocessing import build_preprocessor, ALL_INPUT_FEATURES, TARGET_COLUMN, get_feature_names

def train_and_evaluate_models(csv_path="data/students.csv", model_dir="models"):
    """
    Trains Logistic Regression, Decision Tree, and Random Forest models.
    Evaluates metrics, saves the best model based on F1-score, and outputs model metrics.
    """
    os.makedirs(model_dir, exist_ok=True)
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset file not found at {csv_path}. Please generate synthetic data first.")
        
    df = pd.read_csv(csv_path)
    X = df[ALL_INPUT_FEATURES]
    y = df[TARGET_COLUMN]
    
    # Train / Test split with stratify and fixed random_state=42
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    
    # Base candidate models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=6, min_samples_split=10, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    }
    
    evaluated_results = {}
    fitted_pipelines = {}
    best_name = None
    best_f1 = -1.0
    best_pipeline = None
    
    preprocessor = build_preprocessor()
    
    for name, clf in models.items():
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", clf)
        ])
        
        pipeline.fit(X_train, y_train)
        fitted_pipelines[name] = pipeline
        
        y_pred = pipeline.predict(X_test)
        y_prob = pipeline.predict_proba(X_test)[:, 1] if hasattr(pipeline, "predict_proba") else y_pred
        
        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, zero_division=0))
        rec = float(recall_score(y_test, y_pred, zero_division=0))
        f1 = float(f1_score(y_test, y_pred, zero_division=0))
        auc = float(roc_auc_score(y_test, y_prob))
        
        cm = confusion_matrix(y_test, y_pred).tolist()
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        
        # Feature Importance calculation
        feature_names = get_feature_names(pipeline.named_steps["preprocessor"])
        classifier = pipeline.named_steps["classifier"]
        
        feat_imp = {}
        if hasattr(classifier, "feature_importances_"):
            importances = classifier.feature_importances_
            feat_imp = dict(zip(feature_names, [float(x) for x in importances]))
        elif hasattr(classifier, "coef_"):
            coefs = np.abs(classifier.coef_[0])
            feat_imp = dict(zip(feature_names, [float(x) for x in coefs]))
            
        # Sort feature importances descending
        feat_imp = dict(sorted(feat_imp.items(), key=lambda item: item[1], reverse=True))
        
        evaluated_results[name] = {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(auc, 4),
            "confusion_matrix": cm,
            "roc_curve": {
                "fpr": [round(x, 4) for x in fpr.tolist()],
                "tpr": [round(x, 4) for x in tpr.tolist()]
            },
            "feature_importances": feat_imp
        }
        
        if f1 > best_f1:
            best_f1 = f1
            best_name = name
            best_pipeline = pipeline
            
    # Save best model to joblib
    best_model_path = os.path.join(model_dir, "placement_model.joblib")
    joblib.dump(best_pipeline, best_model_path)
    
    summary = {
        "best_model_name": best_name,
        "best_f1_score": round(best_f1, 4),
        "models": evaluated_results
    }
    
    metrics_path = os.path.join(model_dir, "model_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(summary, f, indent=4)
        
    print(f"Model training complete. Best model '{best_name}' (F1: {best_f1:.4f}) saved to {best_model_path}")
    return summary

if __name__ == "__main__":
    train_and_evaluate_models()
