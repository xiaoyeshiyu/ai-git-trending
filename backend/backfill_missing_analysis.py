import argparse
import sqlite3
import time
from pathlib import Path

from app.github_api import get_repo_details
from app.summarizer import extract_tech_domain, get_summary_for_single_project
from config.logging_config import get_logger
from config.settings import DB_PATH

logger = get_logger('backfill_missing_analysis', 'INFO')


def parse_args():
    parser = argparse.ArgumentParser(description='Backfill missing AI analysis for summarized projects.')
    parser.add_argument('--limit', type=int, default=0, help='Maximum number of missing projects to process. 0 means all.')
    parser.add_argument('--sleep', type=float, default=1.0, help='Sleep seconds between successful requests.')
    return parser.parse_args()


def fetch_missing_projects(limit: int):
    query = """
        SELECT name, url, description, language, stars, forks, contributor_count,
               created_at, updated_at, open_issues, watchers, summary_date, tech_domain
        FROM summarized_projects
        WHERE analysis IS NULL OR TRIM(analysis) = ''
        ORDER BY summary_date DESC, stars DESC
    """
    if limit > 0:
        query += f" LIMIT {int(limit)}"

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute(query).fetchall()


def merge_repo_details(project: dict):
    details = get_repo_details(project['name'])
    if not details:
        return project

    merged = dict(project)
    for key, value in details.items():
        if key == 'tags':
            continue
        if value in (None, '', 'N/A'):
            continue
        merged[key] = value

    return merged


def update_project(project: dict, analysis: str, tech_domain: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            UPDATE summarized_projects
            SET url = ?,
                description = ?,
                language = ?,
                stars = ?,
                forks = ?,
                contributor_count = ?,
                created_at = ?,
                updated_at = ?,
                open_issues = ?,
                watchers = ?,
                tech_domain = ?,
                analysis = ?
            WHERE name = ?
            """,
            (
                project.get('url'),
                project.get('description', 'N/A'),
                project.get('language', 'N/A'),
                int(project.get('stars') or 0),
                int(project.get('forks') or 0),
                int(project.get('contributor_count') or 0),
                project.get('created_at', 'N/A'),
                project.get('updated_at', 'N/A'),
                int(project.get('open_issues') or 0),
                int(project.get('watchers') or 0),
                tech_domain or project.get('tech_domain') or 'Other',
                analysis,
                project['name'],
            ),
        )
        conn.commit()


def main():
    args = parse_args()
    db_path = Path(DB_PATH)
    if not db_path.exists():
        raise SystemExit(f'Database not found: {db_path}')

    rows = fetch_missing_projects(args.limit)
    total = len(rows)
    logger.info(f'Found {total} projects with missing analysis')

    success_count = 0
    failure_count = 0

    for index, row in enumerate(rows, start=1):
        project = dict(row)
        logger.info(f'[{index}/{total}] Backfilling {project["name"]}')
        project = merge_repo_details(project)
        summary = get_summary_for_single_project(project)
        if not summary:
            failure_count += 1
            logger.warning(f'Failed to generate analysis for {project["name"]}')
            continue

        tech_domain = extract_tech_domain(summary, project)
        update_project(project, summary, tech_domain)
        success_count += 1
        logger.info(f'Updated {project["name"]} with tech domain {tech_domain}')
        time.sleep(args.sleep)

    logger.info(f'Backfill completed: success={success_count}, failed={failure_count}')


if __name__ == '__main__':
    main()
