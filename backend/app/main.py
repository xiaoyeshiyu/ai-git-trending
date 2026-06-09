from datetime import datetime, timedelta
from config.settings import AI_ANALYSIS_TTL_DAYS
from .scraper import scrape_github_trending
from .database import ProjectDatabase
from .summarizer import extract_tech_domain, get_summary_for_single_project, get_overview_intro
from .file_writer import save_summary_files
from config.logging_config import get_logger
import time

# 创建日志记录器
logger = get_logger('main', 'INFO')


def _parse_date(date_text):
    try:
        return datetime.strptime(date_text, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def _should_reuse_analysis(cached_project, snapshot_date):
    if not cached_project or not cached_project.get("analysis"):
        return False

    summary_date = _parse_date(cached_project.get("summary_date"))
    if not summary_date:
        return False

    return summary_date >= snapshot_date - timedelta(days=AI_ANALYSIS_TTL_DAYS)


def _build_unavailable_summary(project):
    return f"""### ✨ {project['name']} ({project.get('stars', 0)}★)

> **一句话**：该项目已进入今日 GitHub Trending，但本次暂未成功生成 AI 分析。

- **它是什么**：{project.get('description') or '暂未提供项目描述。'}
- **能解决什么痛点**：暂未提供。
- **适合谁用**：暂未提供。
- **怎么上手**：文档未提供快速上手示例。
- **可以用在哪些场景**：暂未提供。
- **技术看点**：暂未提供。
- **近期动向与发展方向**：暂无 commit 数据可用。
- **同类对比**：暂无明显同类对标。
- **注意事项**：AI 分析暂未生成，建议直接查看项目 README 和 Issue 状态。

- **GitHub**：[{project['name']}]({project.get('url', '')})
"""


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

    projects_for_overview = all_trending_repos

    individual_summaries = []
    analyzed_count = 0
    reused_count = 0
    failed_count = 0
    logger.info(
        f"📝 Preparing {len(projects_for_overview)} trending projects for today's report "
        f"(AI refresh TTL: {AI_ANALYSIS_TTL_DAYS} days)..."
    )
    for project in projects_for_overview:
        cached_project = db.get_summarized_project(project['name'])
        if _should_reuse_analysis(cached_project, snapshot_date):
            summary = cached_project['analysis']
            project['analysis'] = summary
            project['tech_domain'] = cached_project.get('tech_domain') or extract_tech_domain(summary, project)
            individual_summaries.append(summary)
            reused_count += 1
            logger.info(
                f"♻️ Reusing recent AI analysis for {project['name']} "
                f"(last analyzed: {cached_project.get('summary_date')})"
            )
            continue

        summary = get_summary_for_single_project(project)
        if summary:
            individual_summaries.append(summary)
            tech_domain = extract_tech_domain(summary, project)
            project['tech_domain'] = tech_domain
            project['analysis'] = summary
            logger.info(f"🏷️ Tech domain for {project['name']}: {tech_domain}")
            db.add_summarized_project(project)
            analyzed_count += 1
            time.sleep(1)
        else:
            fallback_summary = cached_project.get('analysis') if cached_project else None
            if fallback_summary:
                individual_summaries.append(fallback_summary)
                reused_count += 1
                logger.warning(
                    f"⚠️ Failed to refresh '{project['name']}', using older cached analysis "
                    f"from {cached_project.get('summary_date')}."
                )
            else:
                individual_summaries.append(_build_unavailable_summary(project))
                failed_count += 1
                logger.warning(f"❌ Warning: Failed to summarize '{project['name']}'. Added fallback section.")

    # Always generate and save the daily report
    intro = get_overview_intro(projects_for_overview)
    if individual_summaries:
        final_report = intro + "\n\n" + "\n\n---\n\n".join(individual_summaries)
    else:
        final_report = intro

    save_summary_files(final_report)
    logger.info(
        f"💾 Daily report saved ({len(individual_summaries)} projects: "
        f"{analyzed_count} refreshed, {reused_count} reused, {failed_count} fallback)."
    )

    logger.info(f"✅ Job finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
