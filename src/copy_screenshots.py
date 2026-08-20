import os
import shutil

src_dir = r"C:\Users\srila\.gemini\antigravity-ide\brain\afcd853a-c1ab-4dd9-8928-f1d2dc9454b9"
dest_dir = r"c:\Users\srila\Desktop\College Placement & Skill Gap Analytics\screenshots"
os.makedirs(dest_dir, exist_ok=True)

files = [f for f in os.listdir(src_dir) if f.endswith(".png")]
print("Found PNG files:", files)

for f in files:
    if "dashboard" in f:
        shutil.copy(os.path.join(src_dir, f), os.path.join(dest_dir, "dashboard.png"))
    elif "student_analysis" in f:
        shutil.copy(os.path.join(src_dir, f), os.path.join(dest_dir, "student_analysis.png"))
    elif "placement_prediction" in f:
        shutil.copy(os.path.join(src_dir, f), os.path.join(dest_dir, "prediction.png"))
    elif "skill_gap" in f:
        shutil.copy(os.path.join(src_dir, f), os.path.join(dest_dir, "skill_gap.png"))
    elif "analytics" in f:
        shutil.copy(os.path.join(src_dir, f), os.path.join(dest_dir, "analytics.png"))
    elif "model_performance" in f:
        shutil.copy(os.path.join(src_dir, f), os.path.join(dest_dir, "model_performance.png"))

print("Copied screenshots successfully to", dest_dir)
