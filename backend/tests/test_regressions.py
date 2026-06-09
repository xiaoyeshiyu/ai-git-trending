import os
import sys
import tempfile
import unittest
from datetime import date


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
