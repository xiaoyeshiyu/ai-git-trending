from datetime import datetime
from config.settings import NUM_PROJECTS_TO_SUMMARIZE, DAYS_TO_SKIP
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

    # Get project names that have been summarized recently
    existing_project_names = db.get_all_summarized_project_names()
    
    repos_to_summarize = []
    logger.info(f"🕵️‍♀️ Filtering for {NUM_PROJECTS_TO_SUMMARIZE} new projects to summarize...")
    for repo in all_trending_repos:
        if repo['name'] not in existing_project_names:
            repos_to_summarize.append(repo)
        if len(repos_to_summarize) >= NUM_PROJECTS_TO_SUMMARIZE:
            logger.info(f"👍 Found {len(repos_to_summarize)} new projects to summarize.")
            break

    # Build the report from trending projects (always generate an overview)
    projects_for_overview = all_trending_repos[:NUM_PROJECTS_TO_SUMMARIZE]

    individual_summaries = []
    if repos_to_summarize:
        logger.info(f"📝 Summarizing {len(repos_to_summarize)} new projects...")
        for project in repos_to_summarize:
            summary = get_summary_for_single_project(project)
            if summary:
                individual_summaries.append(summary)
                tech_domain = extract_tech_domain(summary)
                project['tech_domain'] = tech_domain
                logger.info(f"🏷️ Tech domain for {project['name']}: {tech_domain}")
                db.add_summarized_project(project)
                time.sleep(1)
            else:
                logger.warning(f"❌ Warning: Failed to summarize '{project['name']}'. Skipping this project.")
    else:
        logger.info("✅ No new projects to summarize today, generating overview only.")

    # Always generate and save the daily report
    intro = get_overview_intro(projects_for_overview)
    if individual_summaries:
        final_report = intro + "\n\n" + "\n\n---\n\n".join(individual_summaries)
    else:
        final_report = intro + "\n\n> 今日上榜项目此前均已分析，详见历史报告。"

    save_summary_files(final_report)
    logger.info(f"💾 Daily report saved ({len(individual_summaries)} new summaries).")

    logger.info(f"✅ Job finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    