from datetime import datetime
from config.settings import NUM_PROJECTS_TO_SUMMARIZE
from .scraper import scrape_github_trending
from .database import ProjectDatabase
from .summarizer import extract_tech_domain, get_summary_for_single_project, get_overview_intro
from .file_writer import save_summary_files
from config.logging_config import get_logger
import time

# 创建日志记录器
logger = get_logger('main', 'INFO')

def job():
    logger.info(f"🚀 Starting new job at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    db = ProjectDatabase()
    
    all_trending_repos = scrape_github_trending()
    if not all_trending_repos:
        logger.info("⏹️ Job finished: No data scraped.")
        return

    snapshot_date = datetime.now().date()
    logger.info(f"💾 Ingesting {len(all_trending_repos)} projects for date: {snapshot_date.isoformat()}")
    
    # Add rank to each project
    for i, repo_data in enumerate(all_trending_repos):
        repo_data['rank'] = i + 1
        
    # Use the new batch insertion method
    db.add_trending_snapshots(all_trending_repos, snapshot_date)
    
    logger.info(f"✅ Successfully ingested {len(all_trending_repos)} snapshots into the database.")

    # Re-analyze today's top trending projects every run — even if they were
    # summarized before, we want the latest write-up to show up in today's report.
    projects_for_overview = all_trending_repos[:NUM_PROJECTS_TO_SUMMARIZE]

    individual_summaries = []
    logger.info(f"📝 Re-analyzing {len(projects_for_overview)} trending projects for today's report...")
    for project in projects_for_overview:
        summary = get_summary_for_single_project(project)
        if summary:
            individual_summaries.append(summary)
            tech_domain = extract_tech_domain(summary, project)
            project['tech_domain'] = tech_domain
            project['analysis'] = summary
            logger.info(f"🏷️ Tech domain for {project['name']}: {tech_domain}")
            db.add_summarized_project(project)
            time.sleep(1)
        else:
            logger.warning(f"❌ Warning: Failed to summarize '{project['name']}'. Skipping this project.")

    # Always generate and save the daily report
    intro = get_overview_intro(projects_for_overview)
    if individual_summaries:
        final_report = intro + "\n\n" + "\n\n---\n\n".join(individual_summaries)
    else:
        final_report = intro

    save_summary_files(final_report)
    logger.info(f"💾 Daily report saved ({len(individual_summaries)} new summaries).")

    logger.info(f"✅ Job finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    