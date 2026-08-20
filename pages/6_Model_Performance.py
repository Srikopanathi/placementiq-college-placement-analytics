import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.ui_utils import load_application_resources, render_header

# Load metrics data
df_students, quality_report, cleaning_log, sql_engine, metrics_data = load_application_resources()

# Render Header
render_header(
    title="Model Performance Evaluation",
    description="Empirical evaluation matrix and visual diagnostic tools comparing classification models.",
    breadcrumb_suffix="Model Performance"
)

# Best Model Summary Card
st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
st.markdown(f"### Best Performing Model: **{metrics_data['best_model_name']}**")
st.markdown(f"Selected as top candidate based on primary evaluation metric **F1-Score ({metrics_data['best_f1_score']:.4f})**.")

# Evaluation Metrics Table
table_rows = []
for model_name, m in metrics_data["models"].items():
    table_rows.append({
        "Model": model_name,
        "Accuracy": f"{m['accuracy']:.4f}",
        "Precision": f"{m['precision']:.4f}",
        "Recall": f"{m['recall']:.4f}",
        "F1 Score": f"{m['f1_score']:.4f}",
        "ROC-AUC": f"{m['roc_auc']:.4f}"
    })
st.table(pd.DataFrame(table_rows))
st.markdown("</div>", unsafe_allow_html=True)

# Explanation Section
st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
st.markdown("### Metric Explanations")
st.markdown("""
- **Accuracy**: Overall percentage of placement predictions that were correct.
- **Precision**: Among students predicted as placed, how many were actually placed.
- **Recall**: Among students actually placed, how many were correctly identified by the model.
- **F1 Score**: The harmonic mean balancing precision and recall.
- **ROC-AUC**: Evaluates how well the model separates placed vs unplaced candidates across probability thresholds.
""")
st.markdown("</div>", unsafe_allow_html=True)

# Charts Grid (ROC Curve & Feature Importance)
mc_c1, mc_c2 = st.columns(2)
with mc_c1:
    st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
    fig_roc = go.Figure()
    for name, m in metrics_data["models"].items():
        fig_roc.add_trace(go.Scatter(x=m["roc_curve"]["fpr"], y=m["roc_curve"]["tpr"], mode="lines", name=f"{name} (AUC {m['roc_auc']})"))
    fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", line=dict(dash="dash", color="#94A3B8"), name="Baseline"))
    fig_roc.update_layout(title="Receiver Operating Characteristic (ROC)", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_roc, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with mc_c2:
    st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
    selected_model = st.selectbox("Select Model for Feature Importance", list(metrics_data["models"].keys()))
    feat_dict = metrics_data["models"][selected_model]["feature_importances"]
    top10 = dict(list(feat_dict.items())[:10])
    
    df_feat = pd.DataFrame({"Feature": list(top10.keys()), "Importance": list(top10.values())}).sort_values(by="Importance", ascending=True)
    fig_feat = px.bar(df_feat, x="Importance", y="Feature", orientation="h", title=f"Feature Importances ({selected_model})", color_discrete_sequence=["#2563EB"])
    fig_feat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_feat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
