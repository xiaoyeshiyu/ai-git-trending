import os
import sys
import tempfile
import unittest
from datetime import date, timedelta


BACKEND_DIR = os.path.dirname(os.path.dirname(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


from app.database import ProjectDatabase


class ProjectDatabaseTests(unittest.TestCase):
    def test_trending_snapshot_rerun_updates_same_day_metrics_and_project_metadata(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db = ProjectDatabase(os.path.join(tmpdir, "reporter.db"))
            snapshot_date = date(2026, 6, 9)

            db.add_trending_snapshots(
                [
                    {
                        "name": "owner/repo",
                        "url": "https://github.com/owner/repo",
                        "description": "old description",
                        "language": "Python",
                        "rank": 3,
                        "stars": 100,
                        "forks": 10,
                        "tags": ["ai"],
                    }
                ],
                snapshot_date,
            )

            db.add_trending_snapshots(
                [
                    {
                        "name": "owner/repo",
                        "url": "https://github.com/owner/repo",
                        "description": "new description",
                        "language": "TypeScript",
                        "rank": 1,
                        "stars": 150,
                        "forks": 20,
                        "tags": ["ai", "web"],
                    }
                ],
                snapshot_date,
            )

            with db._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT f.rank, f.stars, f.forks, p.description, l.name
                    FROM fact_trending_snapshots f
                    JOIN dim_projects p ON p.project_id = f.project_id
                    LEFT JOIN dim_languages l ON l.language_id = p.language_id
                    """
                )
                self.assertEqual(cursor.fetchone(), (1, 150, 20, "new description", "TypeScript"))

                cursor.execute(
                    """
                    SELECT t.name
                    FROM assoc_project_tags apt
                    JOIN dim_tags t ON t.tag_id = apt.tag_id
                    ORDER BY t.name
                    """
                )
                self.assertEqual([row[0] for row in cursor.fetchall()], ["ai", "web"])


class AnalyzerTests(unittest.TestCase):
    def test_analyze_trends_uses_persisted_tech_domain_distribution(self):
        import app.analyzer as analyzer

        with tempfile.TemporaryDirectory() as tmpdir:
            db = ProjectDatabase(os.path.join(tmpdir, "reporter.db"))
            snapshot_date = date.today()
            db.add_trending_snapshots(
                [
                    {
                        "name": "owner/ai",
                        "url": "https://github.com/owner/ai",
                        "description": "AI project",
                        "language": "Python",
                        "rank": 1,
                        "stars": 100,
                        "forks": 10,
                        "tags": [],
                    },
                    {
                        "name": "owner/web",
                        "url": "https://github.com/owner/web",
                        "description": "Web project",
                        "language": "TypeScript",
                        "rank": 2,
                        "stars": 80,
                        "forks": 5,
                        "tags": [],
                    },
                ],
                snapshot_date,
            )
            db.add_summarized_project({"name": "owner/ai", "tech_domain": "AI/ML", "analysis": "x"})
            db.add_summarized_project({"name": "owner/web", "tech_domain": "Web", "analysis": "x"})

            original_project_database = analyzer.ProjectDatabase
            analyzer.ProjectDatabase = lambda: db
            try:
                trends = analyzer.analyze_trends(7)
            finally:
                analyzer.ProjectDatabase = original_project_database

        self.assertEqual(
            [domain["name"] for domain in trends["techDomains"]],
            ["AI/ML", "Web"],
        )


class ReporterJobTests(unittest.TestCase):
    def test_job_reports_all_today_projects_and_reuses_recent_analysis(self):
        import app.main as main

        today = date.today()
        projects = [
            {"name": "owner/recent", "url": "https://github.com/owner/recent", "description": "recent", "language": "Python", "stars": 3, "forks": 1},
            {"name": "owner/stale", "url": "https://github.com/owner/stale", "description": "stale", "language": "Python", "stars": 2, "forks": 1},
            {"name": "owner/new", "url": "https://github.com/owner/new", "description": "new", "language": "Python", "stars": 1, "forks": 1},
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            db = ProjectDatabase(os.path.join(tmpdir, "reporter.db"))
            with db._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO summarized_projects
                    (name, url, description, language, stars, forks, contributor_count,
                     created_at, updated_at, open_issues, watchers, summary_date, tech_domain, analysis)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        "owner/recent", "https://github.com/owner/recent", "recent", "Python",
                        3, 1, 0, "N/A", "N/A", 0, 0,
                        (today - timedelta(days=7)).isoformat(),
                        "AI/ML", "RECENT ANALYSIS"
                    )
                )
                cursor.execute(
                    """
                    INSERT INTO summarized_projects
                    (name, url, description, language, stars, forks, contributor_count,
                     created_at, updated_at, open_issues, watchers, summary_date, tech_domain, analysis)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        "owner/stale", "https://github.com/owner/stale", "stale", "Python",
                        2, 1, 0, "N/A", "N/A", 0, 0,
                        (today - timedelta(days=15)).isoformat(),
                        "AI/ML", "STALE ANALYSIS"
                    )
                )
                conn.commit()

            analyzed_names = []
            saved_reports = []

            originals = {
                "ProjectDatabase": main.ProjectDatabase,
                "scrape_github_trending": main.scrape_github_trending,
                "get_summary_for_single_project": main.get_summary_for_single_project,
                "get_overview_intro": main.get_overview_intro,
                "save_summary_files": main.save_summary_files,
                "time_sleep": main.time.sleep,
            }
            main.ProjectDatabase = lambda: db
            main.scrape_github_trending = lambda: [dict(project) for project in projects]
            main.get_summary_for_single_project = lambda project: analyzed_names.append(project["name"]) or f"FRESH {project['name']}"
            main.get_overview_intro = lambda overview_projects: "## 今日热点\n具体项目摘要如下："
            main.save_summary_files = saved_reports.append
            main.time.sleep = lambda _: None
            try:
                main.job()
            finally:
                main.ProjectDatabase = originals["ProjectDatabase"]
                main.scrape_github_trending = originals["scrape_github_trending"]
                main.get_summary_for_single_project = originals["get_summary_for_single_project"]
                main.get_overview_intro = originals["get_overview_intro"]
                main.save_summary_files = originals["save_summary_files"]
                main.time.sleep = originals["time_sleep"]

        self.assertEqual(analyzed_names, ["owner/stale", "owner/new"])
        self.assertEqual(len(saved_reports), 1)
        self.assertIn("RECENT ANALYSIS", saved_reports[0])
        self.assertIn("FRESH owner/stale", saved_reports[0])
        self.assertIn("FRESH owner/new", saved_reports[0])


class RouterValidationTests(unittest.TestCase):
    def test_report_date_routes_reject_invalid_dates(self):
        from router import app

        client = app.test_client()

        response = client.get("/api/report/not-a-date")
        self.assertEqual(response.status_code, 400)

        response = client.get("/api/download/not-a-date/md")
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
