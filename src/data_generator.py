import os
import numpy as np
import pandas as pd

def generate_student_data(num_records=3500, random_seed=42):
    """
    Generates synthetic student data for academic placement prediction demonstration.
    Returns a pandas DataFrame with realistic correlations and controlled noise.
    """
    np.random.seed(random_seed)
    
    student_ids = [f"STU{1000 + i}" for i in range(num_records)]
    ages = np.random.choice([19, 20, 21, 22, 23], size=num_records, p=[0.1, 0.35, 0.4, 0.12, 0.03])
    genders = np.random.choice(["Male", "Female", "Other"], size=num_records, p=[0.54, 0.44, 0.02])
    
    branches = np.random.choice(
        ["Computer Science", "Information Technology", "Electronics & Comm", "Electrical Eng", "Mechanical Eng", "Civil Eng"],
        size=num_records,
        p=[0.30, 0.20, 0.20, 0.12, 0.10, 0.08]
    )
    years = np.random.choice([3, 4], size=num_records, p=[0.35, 0.65])
    
    # Academic metrics
    cgpa = np.round(np.clip(np.random.normal(loc=7.6, scale=1.1, size=num_records), 5.0, 10.0), 2)
    attendance = np.round(np.clip(np.random.normal(loc=78, scale=10, size=num_records), 50.0, 100.0), 1)
    
    # Backlog count inversely correlated with CGPA
    p_low = np.array([0.2, 0.3, 0.25, 0.15, 0.07, 0.03])
    p_high = np.array([0.75, 0.15, 0.06, 0.02, 0.01, 0.01])
    backlogs = np.array([
        np.random.choice([0, 1, 2, 3, 4, 5], p=p_low if c < 6.5 else p_high)
        for c in cgpa
    ])
    
    # Practical experience metrics
    internships = np.random.choice([0, 1, 2, 3, 4], size=num_records, p=[0.35, 0.38, 0.18, 0.07, 0.02])
    projects = np.random.choice([0, 1, 2, 3, 4, 5, 6], size=num_records, p=[0.10, 0.22, 0.32, 0.20, 0.10, 0.04, 0.02])
    certifications = np.random.choice(range(11), size=num_records, p=[0.15, 0.25, 0.22, 0.16, 0.10, 0.05, 0.03, 0.02, 0.01, 0.005, 0.005])
    
    # Technical practice: CS/IT students solve more coding problems on average
    is_cs_it = np.isin(branches, ["Computer Science", "Information Technology"])
    coding_base = np.where(is_cs_it, np.random.exponential(scale=90, size=num_records), np.random.exponential(scale=40, size=num_records))
    coding_problems = np.clip(np.round(coding_base).astype(int), 0, 300)
    
    # Technical skill binaries (higher probability for CS/IT and high CGPA)
    skill_prob_boost = (cgpa - 5.0) / 5.0 * 0.25
    
    python = (np.random.rand(num_records) < (0.45 + np.where(is_cs_it, 0.3, 0.0) + skill_prob_boost)).astype(int)
    sql = (np.random.rand(num_records) < (0.40 + np.where(is_cs_it, 0.25, 0.0) + skill_prob_boost)).astype(int)
    java = (np.random.rand(num_records) < (0.35 + np.where(is_cs_it, 0.30, 0.0) + skill_prob_boost)).astype(int)
    dsa = (np.random.rand(num_records) < (0.30 + np.where(is_cs_it, 0.35, 0.0) + (coding_problems / 300.0 * 0.3))).astype(int)
    machine_learning = (np.random.rand(num_records) < (0.20 + np.where(is_cs_it, 0.15, 0.0) + (python * 0.15))).astype(int)
    power_bi = (np.random.rand(num_records) < (0.25 + (sql * 0.15))).astype(int)
    excel = (np.random.rand(num_records) < (0.60 + skill_prob_boost)).astype(int)
    
    # Soft skills
    communication_score = np.round(np.clip(np.random.normal(loc=68, scale=14, size=num_records), 0, 100), 1)
    aptitude_score = np.round(np.clip(np.random.normal(loc=65, scale=15, size=num_records), 0, 100), 1)
    
    # Realistic Target (Placement) Generation
    # Compute continuous logit based on key drivers
    cgpa_norm = (cgpa - 5.0) / 5.0
    intern_norm = internships / 4.0
    proj_norm = projects / 6.0
    coding_norm = coding_problems / 300.0
    comm_norm = communication_score / 100.0
    apt_norm = aptitude_score / 100.0
    skill_sum_norm = (python + sql + java + dsa + machine_learning + power_bi + excel) / 7.0
    backlog_penalty = backlogs * 0.7
    
    logit = (
        -3.2
        + 2.8 * cgpa_norm
        + 1.8 * intern_norm
        + 1.2 * proj_norm
        + 1.4 * coding_norm
        + 1.3 * comm_norm
        + 1.2 * apt_norm
        + 1.5 * skill_sum_norm
        - backlog_penalty
        + 0.4 * (attendance / 100.0)
        + np.random.normal(loc=0.0, scale=0.85, size=num_records)  # Controlled noise
    )
    
    prob = 1.0 / (1.0 + np.exp(-logit))
    placement = (prob >= 0.50).astype(int)
    
    df = pd.DataFrame({
        "student_id": student_ids,
        "age": ages,
        "gender": genders,
        "branch": branches,
        "year": years,
        "cgpa": cgpa,
        "attendance": attendance,
        "backlogs": backlogs,
        "internships": internships,
        "projects": projects,
        "certifications": certifications,
        "coding_problems": coding_problems,
        "python": python,
        "sql": sql,
        "java": java,
        "dsa": dsa,
        "machine_learning": machine_learning,
        "power_bi": power_bi,
        "excel": excel,
        "communication_score": communication_score,
        "aptitude_score": aptitude_score,
        "placement": placement
    })
    
    return df

def save_synthetic_dataset(output_path="data/students.csv", num_records=3500):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = generate_student_data(num_records=num_records)
    df.to_csv(output_path, index=False)
    print(f"Synthetic dataset with {len(df)} records saved to {output_path}")
    return df

if __name__ == "__main__":
    save_synthetic_dataset()
