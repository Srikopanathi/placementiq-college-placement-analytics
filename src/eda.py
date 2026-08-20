import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# SaaS Color System
COLOR_PRIMARY = "#2563EB"       # Indigo / Blue Accent
COLOR_SUCCESS = "#10B981"       # Emerald Green
COLOR_DANGER = "#EF4444"        # Rose Red
COLOR_WARNING = "#F59E0B"       # Amber
COLOR_TEXT = "#0F172A"          # Dark Slate
COLOR_MUTED = "#64748B"         # Muted Slate Text
COLOR_GRID = "#F1F5F9"          # Light Slate Grid
THEME_BG = "rgba(0,0,0,0)"

def apply_saas_layout(fig, title_text="", x_title="", y_title=""):
    """
    Applies consistent SaaS design layout to Plotly figures.
    """
    fig.update_layout(
        title=dict(
            text=title_text,
            font=dict(size=15, color=COLOR_TEXT, family="Inter, system-ui, sans-serif"),
            x=0.0,
            y=0.95
        ),
        paper_bgcolor=THEME_BG,
        plot_bgcolor=THEME_BG,
        font=dict(color=COLOR_MUTED, family="Inter, system-ui, sans-serif", size=12),
        margin=dict(l=20, r=20, t=50, b=40),
        xaxis=dict(
            title=x_title,
            showgrid=True,
            gridcolor=COLOR_GRID,
            zeroline=False,
            title_font=dict(size=12, color=COLOR_MUTED)
        ),
        yaxis=dict(
            title=y_title,
            showgrid=True,
            gridcolor=COLOR_GRID,
            zeroline=False,
            title_font=dict(size=12, color=COLOR_MUTED)
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#E2E8F0",
            borderwidth=1,
            font=dict(size=11, color=COLOR_TEXT)
        )
    )
    return fig

def get_placement_distribution_fig(df):
    placed_counts = df["placement"].map({1: "Placed", 0: "Not Placed"}).value_counts().reset_index()
    placed_counts.columns = ["Status", "Count"]
    fig = px.pie(
        placed_counts,
        names="Status",
        values="Count",
        color="Status",
        color_discrete_map={"Placed": COLOR_SUCCESS, "Not Placed": COLOR_DANGER},
        hole=0.55
    )
    fig.update_traces(textposition='outside', textinfo='percent+label')
    apply_saas_layout(fig, title_text="Overall Placement Distribution")
    return fig

def get_placement_by_cgpa_range_fig(df):
    df_temp = df.copy()
    bins = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    labels = ["5.0 - 6.0", "6.0 - 7.0", "7.0 - 8.0", "8.0 - 9.0", "9.0 - 10.0"]
    df_temp["cgpa_range"] = pd.cut(df_temp["cgpa"], bins=bins, labels=labels, include_lowest=True)
    
    rate_df = df_temp.groupby("cgpa_range", observed=False)["placement"].agg(["count", "mean"]).reset_index()
    rate_df["placement_rate_pct"] = np.round(rate_df["mean"] * 100, 1)
    
    fig = px.bar(
        rate_df,
        x="cgpa_range",
        y="placement_rate_pct",
        text="placement_rate_pct",
        labels={"cgpa_range": "CGPA Bucket", "placement_rate_pct": "Placement Rate (%)"},
        color_discrete_sequence=[COLOR_PRIMARY]
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside', marker_color=COLOR_PRIMARY)
    apply_saas_layout(fig, title_text="Placement Rate by CGPA Range", x_title="CGPA Range", y_title="Placement Rate (%)")
    fig.update_layout(yaxis=dict(range=[0, 115]))
    return fig

def get_placement_by_branch_fig(df):
    branch_df = df.groupby("branch")["placement"].agg(["count", "mean"]).reset_index()
    branch_df["placement_rate_pct"] = np.round(branch_df["mean"] * 100, 1)
    branch_df = branch_df.sort_values(by="placement_rate_pct", ascending=False)
    
    fig = px.bar(
        branch_df,
        x="branch",
        y="placement_rate_pct",
        text="placement_rate_pct",
        labels={"branch": "Branch", "placement_rate_pct": "Placement Rate (%)"},
        color_discrete_sequence=["#4F46E5"]
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    apply_saas_layout(fig, title_text="Placement Rate by Academic Branch", x_title="Branch", y_title="Placement Rate (%)")
    fig.update_layout(yaxis=dict(range=[0, 115]))
    return fig

def get_placement_by_year_fig(df):
    year_df = df.groupby("year")["placement"].agg(["count", "mean"]).reset_index()
    year_df["placement_rate_pct"] = np.round(year_df["mean"] * 100, 1)
    year_df["year_str"] = "Year " + year_df["year"].astype(str)
    
    fig = px.bar(
        year_df,
        x="year_str",
        y="placement_rate_pct",
        text="placement_rate_pct",
        labels={"year_str": "Academic Year", "placement_rate_pct": "Placement Rate (%)"},
        color="year_str",
        color_discrete_sequence=[COLOR_PRIMARY, COLOR_SUCCESS]
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    apply_saas_layout(fig, title_text="Placement Rate by Academic Year", x_title="Academic Year", y_title="Placement Rate (%)")
    fig.update_layout(yaxis=dict(range=[0, 115]))
    return fig

def get_placement_by_internships_fig(df):
    intern_df = df.groupby("internships")["placement"].agg(["count", "mean"]).reset_index()
    intern_df["placement_rate_pct"] = np.round(intern_df["mean"] * 100, 1)
    
    fig = px.line(
        intern_df,
        x="internships",
        y="placement_rate_pct",
        markers=True,
        text="placement_rate_pct",
        labels={"internships": "Internships Completed", "placement_rate_pct": "Placement Rate (%)"}
    )
    fig.update_traces(texttemplate='%{text}%', textposition='top center', line=dict(color=COLOR_SUCCESS, width=3), marker=dict(size=8))
    apply_saas_layout(fig, title_text="Placement Rate vs Internship Count", x_title="Internships", y_title="Placement Rate (%)")
    fig.update_layout(yaxis=dict(range=[0, 115]))
    return fig

def get_placement_by_projects_fig(df):
    proj_df = df.groupby("projects")["placement"].agg(["count", "mean"]).reset_index()
    proj_df["placement_rate_pct"] = np.round(proj_df["mean"] * 100, 1)
    
    fig = px.bar(
        proj_df,
        x="projects",
        y="placement_rate_pct",
        text="placement_rate_pct",
        labels={"projects": "Projects Built", "placement_rate_pct": "Placement Rate (%)"},
        color_discrete_sequence=["#0EA5E9"]
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    apply_saas_layout(fig, title_text="Placement Rate vs Projects Built", x_title="Projects", y_title="Placement Rate (%)")
    fig.update_layout(yaxis=dict(range=[0, 115]))
    return fig

def get_placement_by_coding_fig(df):
    df_temp = df.copy()
    bins = [-1, 25, 75, 150, 225, 300]
    labels = ["0-25", "26-75", "76-150", "151-225", "226-300"]
    df_temp["coding_range"] = pd.cut(df_temp["coding_problems"], bins=bins, labels=labels)
    
    coding_df = df_temp.groupby("coding_range", observed=False)["placement"].agg(["count", "mean"]).reset_index()
    coding_df["placement_rate_pct"] = np.round(coding_df["mean"] * 100, 1)
    
    fig = px.bar(
        coding_df,
        x="coding_range",
        y="placement_rate_pct",
        text="placement_rate_pct",
        labels={"coding_range": "Coding Problems Solved", "placement_rate_pct": "Placement Rate (%)"},
        color_discrete_sequence=["#6366F1"]
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    apply_saas_layout(fig, title_text="Placement Rate by Coding Practice Range", x_title="Coding Problems Range", y_title="Placement Rate (%)")
    fig.update_layout(yaxis=dict(range=[0, 115]))
    return fig

def get_placement_by_backlogs_fig(df):
    backlog_df = df.groupby("backlogs")["placement"].agg(["count", "mean"]).reset_index()
    backlog_df["placement_rate_pct"] = np.round(backlog_df["mean"] * 100, 1)
    
    fig = px.bar(
        backlog_df,
        x="backlogs",
        y="placement_rate_pct",
        text="placement_rate_pct",
        labels={"backlogs": "Backlog Count", "placement_rate_pct": "Placement Rate (%)"},
        color_discrete_sequence=["#F43F5E"]
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    apply_saas_layout(fig, title_text="Placement Rate by Backlogs Count", x_title="Backlogs", y_title="Placement Rate (%)")
    fig.update_layout(yaxis=dict(range=[0, 115]))
    return fig

def get_skill_distribution_and_placement_fig(df):
    skills = ["python", "sql", "java", "dsa", "machine_learning", "power_bi", "excel"]
    records = []
    for s in skills:
        total_with_skill = df[s].sum()
        placed_with_skill = df[df[s] == 1]["placement"].mean() * 100 if total_with_skill > 0 else 0
        records.append({
            "Skill": s.upper().replace("_", " "),
            "Student Count": total_with_skill,
            "Placement Rate (%)": round(placed_with_skill, 1)
        })
    skill_df = pd.DataFrame(records).sort_values(by="Placement Rate (%)", ascending=False)
    
    fig = px.bar(
        skill_df,
        x="Skill",
        y="Placement Rate (%)",
        text="Placement Rate (%)",
        color_discrete_sequence=["#8B5CF6"]
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    apply_saas_layout(fig, title_text="Placement Rate by Technical Skill", x_title="Skill", y_title="Placement Rate (%)")
    fig.update_layout(yaxis=dict(range=[0, 115]))
    return fig

def get_top_skill_gaps_fig(df):
    """
    Returns horizontal bar chart of top missing skills across all students.
    """
    skills = ["python", "sql", "java", "dsa", "machine_learning", "power_bi", "excel"]
    total = len(df)
    missing_records = []
    for s in skills:
        missing_count = total - int(df[s].sum())
        missing_pct = round((missing_count / total) * 100, 1) if total > 0 else 0
        missing_records.append({
            "Skill": s.upper().replace("_", " "),
            "Missing Count": missing_count,
            "Missing Pct": missing_pct
        })
    df_missing = pd.DataFrame(missing_records).sort_values(by="Missing Count", ascending=True)
    
    fig = px.bar(
        df_missing,
        x="Missing Count",
        y="Skill",
        orientation="h",
        text="Missing Count",
        color_discrete_sequence=["#F59E0B"]
    )
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    apply_saas_layout(fig, title_text="Top Missing Technical Skill Gaps", x_title="Student Count Missing Skill", y_title="Skill")
    return fig

def get_correlation_heatmap_fig(df):
    num_cols = ["cgpa", "attendance", "backlogs", "internships", "projects", 
                "certifications", "coding_problems", "communication_score", "aptitude_score", "placement"]
    corr_matrix = df[num_cols].corr().round(2)
    
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="Blues",
        aspect="auto"
    )
    apply_saas_layout(fig, title_text="Feature Correlation Matrix Heatmap")
    return fig

def get_cgpa_vs_placement_boxplot(df):
    df_temp = df.copy()
    df_temp["Status"] = df_temp["placement"].map({1: "Placed", 0: "Not Placed"})
    fig = px.box(
        df_temp,
        x="Status",
        y="cgpa",
        color="Status",
        color_discrete_map={"Placed": COLOR_SUCCESS, "Not Placed": COLOR_DANGER},
        points="outliers"
    )
    apply_saas_layout(fig, title_text="CGPA Distribution: Placed vs Unplaced Students", x_title="Status", y_title="CGPA")
    return fig

def get_coding_vs_comm_scatter_fig(df):
    df_temp = df.copy()
    df_temp["Status"] = df_temp["placement"].map({1: "Placed", 0: "Not Placed"})
    fig = px.scatter(
        df_temp,
        x="coding_problems",
        y="communication_score",
        color="Status",
        size="cgpa",
        hover_data=["student_id", "branch", "internships"],
        color_discrete_map={"Placed": COLOR_SUCCESS, "Not Placed": COLOR_DANGER},
        opacity=0.75
    )
    apply_saas_layout(fig, title_text="Coding Problems Solved vs Communication Score (Size = CGPA)", x_title="Coding Problems", y_title="Communication Score")
    return fig
