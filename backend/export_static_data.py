"""Export database data to static JSON files for GitHub Pages."""

import json
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from app.database import ProjectDatabase

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs', 'data')
MD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'md')


def export():
    db = ProjectDatabase()
    os.makedirs(os.path.join(OUTPUT_DIR, 'reports'), exist_ok=True)

    # 1. Reports list
    reports = []
    if os.path.isdir(MD_DIR):
        for f in sorted(os.listdir(MD_DIR), reverse=True):
            if f.endswith('.md'):
                date_str = f.replace('github_trending_', '').replace('.md', '')
                filepath = os.path.join(MD_DIR, f)
                with open(filepath, 'r') as fh:
                    content = fh.read()
                project_count = content.count('### ✨')
                reports.append({
                    "date": date_str,
                    "project_count": project_count if project_count > 0 else 0
                })
                # Export individual report content
                report_data = {
                    "date": date_str,
                    "content": content,
                    "project_count": project_count if project_count > 0 else 0
                }
                report_dir = os.path.join(OUTPUT_DIR, 'reports')
                os.makedirs(report_dir, exist_ok=True)
                with open(os.path.join(report_dir, f'{date_str}.json'), 'w') as fh:
                    json.dump(report_data, fh, ensure_ascii=False)

    with open(os.path.join(OUTPUT_DIR, 'reports.json'), 'w') as f:
        json.dump(reports, f, ensure_ascii=False)
    print(f"Exported {len(reports)} reports")

    # 2. Stats
    stats = {"totalReports": len(reports), "totalProjects": 0, "topLanguage": "N/A",
             "weeklyNew": 0, "totalForks": "0", "avgContributors": 0, "activityScore": 20}
    try:
        with db._get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM summarized_projects")
            stats["totalProjects"] = c.fetchone()[0]
            c.execute("SELECT language, COUNT(*) as cnt FROM summarized_projects WHERE language != 'N/A' AND language IS NOT NULL GROUP BY language ORDER BY cnt DESC LIMIT 1")
            row = c.fetchone()
            if row:
                stats["topLanguage"] = row[0]
            week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            c.execute("SELECT COUNT(*) FROM summarized_projects WHERE summary_date >= ?", (week_ago,))
            stats["weeklyNew"] = c.fetchone()[0]
            c.execute("SELECT SUM(forks) FROM summarized_projects")
            total_forks = c.fetchone()[0] or 0
            stats["totalForks"] = f"{total_forks:,}"
            c.execute("SELECT AVG(contributor_count) FROM summarized_projects WHERE contributor_count != 'N/A'")
            avg = c.fetchone()[0] or 0
            stats["avgContributors"] = round(avg, 1)
    except Exception as e:
        print(f"Stats warning: {e}")

    with open(os.path.join(OUTPUT_DIR, 'stats.json'), 'w') as f:
        json.dump(stats, f, ensure_ascii=False)
    print(f"Exported stats: {stats['totalProjects']} projects")

    # 3. Projects index (for library/rankings)
    try:
        with db._get_connection() as conn:
            c = conn.cursor()
            c.execute("""
                SELECT name, url, description, language, stars, forks,
                       contributor_count, created_at, updated_at, open_issues,
                       watchers, summary_date, tech_domain, analysis
                FROM summarized_projects ORDER BY stars DESC
            """)
            rows = c.fetchall()
            projects = []
            for r in rows:
                projects.append({
                    "name": r[0], "url": r[1], "description": r[2],
                    "language": r[3], "stars": r[4], "forks": r[5],
                    "contributor_count": r[6], "created_at": r[7],
                    "updated_at": r[8], "open_issues": r[9],
                    "watchers": r[10], "summary_date": r[11],
                    "tech_domain": r[12] or "Other",
                    "analysis": r[13] or ""
                })
        with open(os.path.join(OUTPUT_DIR, 'projects.json'), 'w') as f:
            json.dump(projects, f, ensure_ascii=False)
        print(f"Exported {len(projects)} projects")
    except Exception as e:
        print(f"Projects warning: {e}")

    # 4. Trends data (for trend tabs on static site)
    try:
        from app.analyzer import analyze_trends
        trends_7d = analyze_trends(7)
        trends_30d = analyze_trends(30)
        trends = {
            "daily": trends_7d,
            "monthly": trends_30d,
            "updated_at": datetime.now().isoformat()
        }
        with open(os.path.join(OUTPUT_DIR, 'trends.json'), 'w') as f:
            json.dump(trends, f, ensure_ascii=False)
        print(f"Exported trends data (7d: {len(trends_7d.get('most_frequent_projects',[]))} projects, 30d: {len(trends_30d.get('most_frequent_projects',[]))} projects)")
    except Exception as e:
        print(f"Trends warning: {e}")

    # 5. Language distribution
    try:
        with db._get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT language, COUNT(*) as cnt FROM summarized_projects WHERE language != 'N/A' AND language IS NOT NULL GROUP BY language ORDER BY cnt DESC")
            languages = [{"name": r[0], "count": r[1]} for r in c.fetchall()]
        with open(os.path.join(OUTPUT_DIR, 'languages.json'), 'w') as f:
            json.dump(languages, f, ensure_ascii=False)
        print(f"Exported {len(languages)} languages")
    except Exception as e:
        print(f"Languages warning: {e}")

    print("Static data export complete.")


if __name__ == '__main__':
    export()
