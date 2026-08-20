ROLE_REQUIREMENTS = {
    "Data Analyst": {
        "binary_skills": ["python", "sql", "excel", "power_bi"],
        "min_comm_score": 65,
        "min_aptitude_score": 65,
        "min_coding_problems": 30,
        "min_projects": 2
    },
    "Machine Learning Engineer": {
        "binary_skills": ["python", "sql", "machine_learning", "dsa"],
        "min_comm_score": 60,
        "min_aptitude_score": 70,
        "min_coding_problems": 100,
        "min_projects": 2
    },
    "Software Developer": {
        "binary_skills": ["dsa", "sql"], # Needs either python or java
        "any_of_skills": [["python", "java"]],
        "min_comm_score": 65,
        "min_aptitude_score": 65,
        "min_coding_problems": 120,
        "min_projects": 2
    }
}

class SkillGapAnalyzer:
    """
    Analyzes student technical and soft skill profile against specific target career roles.
    """
    @staticmethod
    def analyze_student_role_gap(student_data: dict, target_role: str) -> dict:
        if target_role not in ROLE_REQUIREMENTS:
            target_role = "Data Analyst"
            
        reqs = ROLE_REQUIREMENTS[target_role]
        matching_skills = []
        missing_skills = []
        
        # Check required binary skills
        for skill in reqs.get("binary_skills", []):
            skill_name = skill.upper().replace("_", " ")
            if student_data.get(skill, 0) == 1:
                matching_skills.append(skill_name)
            else:
                priority = "High" if skill in ["python", "sql", "dsa", "machine_learning"] else "Medium"
                missing_skills.append({
                    "skill": skill_name,
                    "key": skill,
                    "priority": priority,
                    "reason": f"Required core technical competency for {target_role}."
                })
                
        # Check OR skills if applicable
        if "any_of_skills" in reqs:
            for group in reqs["any_of_skills"]:
                has_any = any(student_data.get(s, 0) == 1 for s in group)
                group_names = " / ".join([s.upper().replace("_", " ") for s in group])
                if has_any:
                    matching_skills.append(f"Programming ({group_names})")
                else:
                    missing_skills.append({
                        "skill": f"Programming Language ({group_names})",
                        "key": group[0],
                        "priority": "High",
                        "reason": f"At least one core programming language is required for {target_role}."
                    })
                    
        # Check practical coding problem count
        coding_count = student_data.get("coding_problems", 0)
        min_coding = reqs.get("min_coding_problems", 50)
        if coding_count >= min_coding:
            matching_skills.append(f"Coding Practice ({coding_count} solved)")
        else:
            missing_skills.append({
                "skill": f"Coding Problem Practice ({min_coding}+ required)",
                "key": "coding_problems",
                "priority": "High" if coding_count < min_coding / 2 else "Medium",
                "reason": f"Currently solved {coding_count} problems. Target role requires strong problem solving."
            })
            
        # Check projects count
        projects_count = student_data.get("projects", 0)
        min_proj = reqs.get("min_projects", 2)
        if projects_count >= min_proj:
            matching_skills.append(f"Project Portfolio ({projects_count} projects)")
        else:
            missing_skills.append({
                "skill": f"Hands-on Projects ({min_proj}+ required)",
                "key": "projects",
                "priority": "Medium",
                "reason": f"Currently completed {projects_count} projects. Practical build experience needed."
            })
            
        # Check soft skills
        comm_score = student_data.get("communication_score", 0)
        min_comm = reqs.get("min_comm_score", 60)
        if comm_score >= min_comm:
            matching_skills.append(f"Communication Skill ({comm_score}/100)")
        else:
            missing_skills.append({
                "skill": "Communication & Interview Prep",
                "key": "communication_score",
                "priority": "High" if comm_score < 50 else "Medium",
                "reason": f"Score of {comm_score} is below role benchmark of {min_comm}."
            })
            
        apt_score = student_data.get("aptitude_score", 0)
        min_apt = reqs.get("min_aptitude_score", 60)
        if apt_score >= min_apt:
            matching_skills.append(f"Quantitative Aptitude ({apt_score}/100)")
        else:
            missing_skills.append({
                "skill": "Quantitative & Logical Aptitude",
                "key": "aptitude_score",
                "priority": "Medium",
                "reason": f"Score of {apt_score} is below role benchmark of {min_apt}."
            })
            
        total_eval_items = len(matching_skills) + len(missing_skills)
        gap_percentage = round((len(missing_skills) / total_eval_items) * 100, 1) if total_eval_items > 0 else 0
        match_percentage = round(100 - gap_percentage, 1)
        
        return {
            "target_role": target_role,
            "match_percentage": match_percentage,
            "gap_percentage": gap_percentage,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "total_items_evaluated": total_eval_items
        }
