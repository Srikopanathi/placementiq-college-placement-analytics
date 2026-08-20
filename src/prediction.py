import os
import joblib
import pandas as pd
import numpy as np

# Configurable Risk Thresholds
HIGH_RISK_THRESHOLD = 0.40
MEDIUM_RISK_THRESHOLD = 0.70

class PlacementPredictor:
    def __init__(self, model_path="models/placement_model.joblib"):
        self.model_path = model_path
        self.pipeline = None
        self.load_model()
        
    def load_model(self):
        if os.path.exists(self.model_path):
            self.pipeline = joblib.load(self.model_path)
        else:
            self.pipeline = None
            
    def predict_student(self, student_data: dict) -> dict:
        """
        Takes a single student's feature dictionary and computes live placement inference.
        Returns probability, predicted status, risk level, and main contributing factors.
        """
        if self.pipeline is None:
            self.load_model()
            if self.pipeline is None:
                raise RuntimeError("Placement model not loaded. Please train the model first.")
                
        df_input = pd.DataFrame([student_data])
        
        # Predict probability & binary target
        prob = float(self.pipeline.predict_proba(df_input)[0, 1])
        predicted_class = int(self.pipeline.predict(df_input)[0])
        
        status = "Likely Placed" if predicted_class == 1 else "At Risk"
        
        if prob < HIGH_RISK_THRESHOLD:
            risk_level = "HIGH"
        elif prob <= MEDIUM_RISK_THRESHOLD:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
            
        # Determine main positive & negative factors dynamically
        factors = []
        cgpa = student_data.get("cgpa", 0)
        internships = student_data.get("internships", 0)
        projects = student_data.get("projects", 0)
        coding = student_data.get("coding_problems", 0)
        backlogs = student_data.get("backlogs", 0)
        comm = student_data.get("communication_score", 0)
        apt = student_data.get("aptitude_score", 0)
        
        if cgpa >= 7.5:
            factors.append(("Strong Academic Record (CGPA)", "Positive"))
        else:
            factors.append(("Lower Academic Grade (CGPA < 7.5)", "Negative"))
            
        if internships >= 1:
            factors.append(("Practical Industry Internship Experience", "Positive"))
        else:
            factors.append(("No Internship Experience", "Negative"))
            
        if coding >= 100:
            factors.append(("Substantial Coding Problem Practice", "Positive"))
        elif coding < 40:
            factors.append(("Limited Coding Practice (<40 solved)", "Negative"))
            
        if backlogs > 0:
            factors.append((f"Active Backlogs Present ({backlogs})", "Negative"))
        else:
            factors.append(("Clear Academic Standing (Zero Backlogs)", "Positive"))
            
        if comm < 60:
            factors.append(("Communication Score Needs Enhancement", "Negative"))
        if apt < 60:
            factors.append(("Aptitude Score Needs Improvement", "Negative"))
            
        return {
            "probability_pct": round(prob * 100, 1),
            "probability_raw": prob,
            "status": status,
            "risk_level": risk_level,
            "contributing_factors": factors
        }
