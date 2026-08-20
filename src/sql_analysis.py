import os
import sqlite3
import pandas as pd

class SQLAnalyticsEngine:
    def __init__(self, db_path="database/placement.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
    def get_connection(self):
        return sqlite3.connect(self.db_path)
        
    def initialize_database(self, df: pd.DataFrame):
        """
        Loads the student DataFrame into the SQLite 'students' table.
        """
        conn = self.get_connection()
        df.to_sql("students", conn, if_exists="replace", index=False)
        conn.commit()
        conn.close()
        
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Executes an arbitrary SQL query and returns results as a pandas DataFrame.
        """
        conn = self.get_connection()
        result_df = pd.read_sql_query(query, conn)
        conn.close()
        return result_df
        
    def get_predefined_insights(self) -> dict:
        """
        Runs key SQL queries for the PlacementIQ SQL Insights section.
        Returns dictionary of query titles, query SQL strings, and result DataFrames.
        """
        queries = {
            "overall_placement": {
                "title": "1. Overall Placement Rate & Counts",
                "sql": """
                    SELECT 
                        COUNT(*) as total_students,
                        SUM(placement) as placed_students,
                        COUNT(*) - SUM(placement) as unplaced_students,
                        ROUND(AVG(placement) * 100, 2) as placement_rate_pct
                    FROM students;
                """
            },
            "placement_by_branch": {
                "title": "2. Placement Rate by Branch",
                "sql": """
                    SELECT 
                        branch,
                        COUNT(*) as total_students,
                        SUM(placement) as placed_students,
                        ROUND(AVG(placement) * 100, 2) as placement_rate_pct,
                        ROUND(AVG(cgpa), 2) as avg_cgpa
                    FROM students
                    GROUP BY branch
                    ORDER BY placement_rate_pct DESC;
                """
            },
            "placement_by_year": {
                "title": "3. Placement Rate by Academic Year",
                "sql": """
                    SELECT 
                        year,
                        COUNT(*) as total_students,
                        SUM(placement) as placed_students,
                        ROUND(AVG(placement) * 100, 2) as placement_rate_pct
                    FROM students
                    GROUP BY year
                    ORDER BY year;
                """
            },
            "placed_vs_unplaced_academics": {
                "title": "4. Academic & Practical Comparison (Placed vs Unplaced)",
                "sql": """
                    SELECT 
                        CASE WHEN placement = 1 THEN 'Placed' ELSE 'Unplaced' END as status,
                        COUNT(*) as count,
                        ROUND(AVG(cgpa), 2) as avg_cgpa,
                        ROUND(AVG(internships), 2) as avg_internships,
                        ROUND(AVG(projects), 2) as avg_projects,
                        ROUND(AVG(coding_problems), 1) as avg_coding_problems,
                        ROUND(AVG(communication_score), 1) as avg_comm_score,
                        ROUND(AVG(aptitude_score), 1) as avg_aptitude_score
                    FROM students
                    GROUP BY placement;
                """
            },
            "high_cgpa_no_internship": {
                "title": "5. High CGPA (≥ 8.0) Students with Zero Internships",
                "sql": """
                    SELECT 
                        student_id, branch, year, cgpa, internships, coding_problems, placement
                    FROM students
                    WHERE cgpa >= 8.0 AND internships = 0
                    ORDER BY cgpa DESC
                    LIMIT 10;
                """
            },
            "strong_coder_weak_comm": {
                "title": "6. Strong Coders (≥150 problems) with Weak Communication (<60)",
                "sql": """
                    SELECT 
                        student_id, branch, coding_problems, communication_score, cgpa, placement
                    FROM students
                    WHERE coding_problems >= 150 AND communication_score < 60
                    ORDER BY coding_problems DESC
                    LIMIT 10;
                """
            },
            "high_risk_students": {
                "title": "7. High Placement Risk Students (Low CGPA & Active Backlogs)",
                "sql": """
                    SELECT 
                        student_id, branch, year, cgpa, backlogs, attendance, internships, placement
                    FROM students
                    WHERE cgpa < 6.5 AND backlogs > 0
                    ORDER BY backlogs DESC, cgpa ASC
                    LIMIT 15;
                """
            },
            "missing_skills_distribution": {
                "title": "8. Most Common Missing Skills Across All Students",
                "sql": """
                    SELECT 
                        'Python' as skill, COUNT(*) - SUM(python) as missing_count, ROUND((1.0 - AVG(python))*100, 1) as missing_pct FROM students
                    UNION ALL
                    SELECT 'SQL', COUNT(*) - SUM(sql), ROUND((1.0 - AVG(sql))*100, 1) FROM students
                    UNION ALL
                    SELECT 'Java', COUNT(*) - SUM(java), ROUND((1.0 - AVG(java))*100, 1) FROM students
                    UNION ALL
                    SELECT 'Data Structures & Algo (DSA)', COUNT(*) - SUM(dsa), ROUND((1.0 - AVG(dsa))*100, 1) FROM students
                    UNION ALL
                    SELECT 'Machine Learning', COUNT(*) - SUM(machine_learning), ROUND((1.0 - AVG(machine_learning))*100, 1) FROM students
                    UNION ALL
                    SELECT 'Power BI', COUNT(*) - SUM(power_bi), ROUND((1.0 - AVG(power_bi))*100, 1) FROM students
                    UNION ALL
                    SELECT 'Excel', COUNT(*) - SUM(excel), ROUND((1.0 - AVG(excel))*100, 1) FROM students
                    ORDER BY missing_count DESC;
                """
            },
            "placement_by_internship_brackets": {
                "title": "9. Placement Success Rate by Internship Experience Bracket",
                "sql": """
                    SELECT 
                        CASE 
                            WHEN internships = 0 THEN '0 Internships'
                            WHEN internships = 1 THEN '1 Internship'
                            ELSE '2+ Internships'
                        END as internship_bracket,
                        COUNT(*) as total_students,
                        SUM(placement) as placed_count,
                        ROUND(AVG(placement) * 100, 2) as placement_rate_pct
                    FROM students
                    GROUP BY internship_bracket
                    ORDER BY placement_rate_pct DESC;
                """
            },
            "coding_problems_tiers": {
                "title": "10. Coding Practice Tiers vs Placement Outcome",
                "sql": """
                    SELECT 
                        CASE 
                            WHEN coding_problems < 50 THEN 'Beginner (<50)'
                            WHEN coding_problems BETWEEN 50 AND 150 THEN 'Intermediate (50-150)'
                            ELSE 'Advanced (150+)'
                        END as coding_tier,
                        COUNT(*) as total_students,
                        SUM(placement) as placed_students,
                        ROUND(AVG(placement) * 100, 2) as placement_rate_pct,
                        ROUND(AVG(cgpa), 2) as avg_cgpa
                    FROM students
                    GROUP BY coding_tier
                    ORDER BY placement_rate_pct DESC;
                """
            }
        }
        
        results = {}
        for key, info in queries.items():
            results[key] = {
                "title": info["title"],
                "sql": info["sql"],
                "data": self.execute_query(info["sql"])
            }
        return results
