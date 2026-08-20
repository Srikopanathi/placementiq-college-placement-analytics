# PlacementIQ — Project Metrics

## Dataset
- **Dataset Filename**: `data/students.csv`
- **Total Records**: 3,500
- **Total Raw Features**: 22
- **Placed Count**: 3,097
- **Not Placed Count**: 403
- **Placement Rate**: 88.49%

## Data Quality
- **Missing Values**: 0
- **Duplicates**: 0
- **Data Integrity Status**: PASSED (Clean)

## Machine Learning
- **Models Compared**: 3 (Logistic Regression, Decision Tree, Random Forest)
- **Best Model Selected**: Random Forest
- **Evaluation Split**: 80% Train / 20% Test (Stratified, `random_state=42`)
- **Primary Metric**: F1 Score

### Best Model Performance (Random Forest)
- **Accuracy**: 0.9343 (93.43%)
- **Precision**: 0.9428 (94.28%)
- **Recall**: 0.9855 (98.55%)
- **F1 Score**: 0.9637 (96.37%)
- **ROC-AUC**: 0.9236

### Candidate Models Comparison
| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Logistic Regression | 0.9271 | 0.9479 | 0.9709 | 0.9593 | 0.9421 |
| Decision Tree | 0.9157 | 0.9473 | 0.9580 | 0.9526 | 0.8286 |
| Random Forest | 0.9343 | 0.9428 | 0.9855 | 0.9637 | 0.9236 |

## Feature Engineering
- **Original Feature Count**: 20
- **Final ML Features**: 24 (One-Hot Encoded & Scaled)
- **Top 5 Contributing Features**:
  - `backlogs`: 0.2661
  - `cgpa`: 0.2205
  - `aptitude_score`: 0.0665
  - `coding_problems`: 0.0635
  - `communication_score`: 0.0628

## Analytics & Database
- **SQL Queries Executed**: 10
- **KPI Metrics Tracked**: 5 (Total Students, Placement Rate, Avg CGPA, Avg Coding, High-Risk Count)
- **Career Roles Benchmarked**: 3 (Data Analyst, ML Engineer, Software Developer)

## Application Architecture
- **Navigation Pages**: 9 Independent Pages
- **Routing Engine**: Streamlit Multipage (`st.navigation`, `st.Page`)
- **CSV Export Feature**: Integrated in Placement Officer Desk
