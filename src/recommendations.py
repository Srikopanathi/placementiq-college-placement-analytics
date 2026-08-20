class RecommendationEngine:
    """
    Generates dynamic, rule-based recommendations tailored to a student's metrics and target role.
    """
    @staticmethod
    def generate_recommendations(student_data: dict, target_role: str = None) -> list:
        recs = []
        
        # 1. Backlog remediation
        backlogs = student_data.get("backlogs", 0)
        if backlogs > 0:
            recs.append({
                "priority": "HIGH",
                "skill": "Academic Backlogs Clearance",
                "reason": f"Student has {backlogs} active backlog(s). Many tier-1 recruiters filter out candidates with active backlogs.",
                "action": "Prioritize clearing active backlog examinations before campus placement drives begin."
            })
            
        # 2. Internships recommendation
        internships = student_data.get("internships", 0)
        if internships == 0:
            recs.append({
                "priority": "HIGH",
                "skill": "Practical Industry Internship",
                "reason": "Zero internship experience recorded. Placed students have 1.8x higher internship participation.",
                "action": "Apply for 8–12 week industry internships or virtual pre-placement industrial training programs."
            })
            
        # 3. Coding problem practice
        coding = student_data.get("coding_problems", 0)
        if coding < 50:
            recs.append({
                "priority": "HIGH",
                "skill": "Data Structures & Algorithmic Problem Solving",
                "reason": f"Only {coding} coding problems solved. Technical rounds require strong DSA problem solving speed.",
                "action": "Solve 3-5 coding problems daily on platforms like LeetCode, HackerRank, or Code360 to reach at least 120+ solved."
            })
            
        # 4. Project portfolio
        projects = student_data.get("projects", 0)
        if projects < 2:
            recs.append({
                "priority": "HIGH",
                "skill": "Practical Portfolio Projects",
                "reason": f"Student has built {projects} project(s). Recruiters expect candidate portfolio links during interviews.",
                "action": "Build at least 2 end-to-end domain projects (e.g. Full-stack app, Data Analytics pipeline) hosted on GitHub."
            })
            
        # 5. Core technical skills (SQL & Programming)
        if student_data.get("sql", 0) == 0:
            recs.append({
                "priority": "HIGH",
                "skill": "SQL Fundamentals & Relational Databases",
                "reason": "SQL is a mandatory technical round filter across Software, Analytics, and Data roles.",
                "action": "Complete a structured SQL course covering JOINs, aggregations, subqueries, and window functions."
            })
            
        if student_data.get("python", 0) == 0 and student_data.get("java", 0) == 0:
            recs.append({
                "priority": "HIGH",
                "skill": "Core Programming Language (Python or Java)",
                "reason": "Missing fundamental Object-Oriented Programming (OOP) language certification.",
                "action": "Learn Python or Java core fundamentals, data types, OOP concepts, and standard libraries."
            })
            
        # 6. Target-role specific recommendations
        if target_role == "Data Analyst":
            if student_data.get("power_bi", 0) == 0 and student_data.get("excel", 0) == 0:
                recs.append({
                    "priority": "HIGH",
                    "skill": "Business Intelligence (Power BI / Advanced Excel)",
                    "reason": "Targeting Data Analyst role without dashboard visualization tools.",
                    "action": "Build 2 interactive Power BI/Tableau dashboards showcasing KPI metrics and business insights."
                })
        elif target_role == "Machine Learning Engineer":
            if student_data.get("machine_learning", 0) == 0:
                recs.append({
                    "priority": "HIGH",
                    "skill": "Machine Learning & Scikit-learn Pipelines",
                    "reason": "Targeting ML Engineer role without verified Machine Learning coursework.",
                    "action": "Implement supervised and unsupervised ML models using Pandas, NumPy, and Scikit-learn."
                })
        elif target_role == "Software Developer":
            if student_data.get("dsa", 0) == 0:
                recs.append({
                    "priority": "HIGH",
                    "skill": "Data Structures & Algorithms (Trees, Graphs, DP)",
                    "reason": "Targeting Software Developer role without formal DSA knowledge.",
                    "action": "Master Array, Linked List, Stack, Queue, Tree, Graph, and Dynamic Programming algorithms."
                })
                
        # 7. Soft skills & interview readiness
        comm = student_data.get("communication_score", 0)
        if comm < 60:
            recs.append({
                "priority": "MEDIUM",
                "skill": "Communication & Interview Expression",
                "reason": f"Communication score of {comm}/100 indicates risk in HR and Technical interview rounds.",
                "action": "Participate in mock interviews, campus Toastmasters sessions, and English communication practice."
            })
            
        apt = student_data.get("aptitude_score", 0)
        if apt < 60:
            recs.append({
                "priority": "MEDIUM",
                "skill": "Quantitative & Logical Aptitude",
                "reason": f"Aptitude score of {apt}/100 is below the online placement screening cutoff.",
                "action": "Practice timed quantitative aptitude, logical reasoning, and verbal tests on IndiaBIX or GeeksforGeeks."
            })
            
        # Sort recommendations by priority (HIGH before MEDIUM)
        priority_map = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        recs.sort(key=lambda x: priority_map.get(x["priority"], 9))
        return recs
