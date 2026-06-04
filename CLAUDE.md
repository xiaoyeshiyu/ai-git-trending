# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GitHub Trending Reporter — an automated bot that scrapes GitHub Trending daily, uses an LLM (OpenAI-compatible API) to analyze/summarize projects in Chinese, generates Markdown + HTML reports, and serves an interactive Vue 3 web dashboard.

## Commands

### Backend (Python 3.12, Flask)

```bash
cd backend
pip install -r requirements.txt

# Full service (web API + scheduled reporter)
python app.py

# Web API only (dev)
python app.py --mode web --debug

# Single reporter run (CI/CD mode)
python app.py --mode reporter --once

# Export DB data to static JSON files (for GitHub Pages)
python export_static_data.py
```

### Frontend (Vue 3 + TypeScript + Vite)

```bash
cd frontend
npm install
npm run dev         # dev server on :5173, proxies /api → :5001
npm run build       # type-check + production build
npm run type-check  # vue-tsc only
npm run lint        # ESLint
npm run format      # Prettier

# GitHub Pages static build (reads docs/data/*.json instead of live API)
VITE_STATIC_MODE=true npx vite build --base=/ai-git-trending/ --outDir=../docs
```

### Docker

```bash
docker build -t git-trending:latest .
docker run --env-file .env -p 5001:5001 git-trending:latest
```

## Architecture

### Data Flow

```
GitHub Trending HTML  ──scraper.py──►  repo list
                                         │
                              ┌──────────┴──────────┐
                              ▼                     ▼
                     github_api.py          summarized_projects
                      (GH REST API)           (SQLite table)
                              │                     │
                              ▼                     ▼
                         summarizer.py  ◄──  filter new projects
                       (LLM via httpx)         (skip already-summarized)
                              │
                              ▼
                        file_writer.py
                     (MD + HTML output)
                              │
                              ▼
                        notifier.py
                (DingTalk / Feishu / ClawBot)
```

### Database Schema (SQLite)

Two parallel access layers exist — prefer `database.py` (raw sqlite3) for current code:

- **Star schema** for historical analysis:
  - `dim_projects`, `dim_languages`, `dim_tags`, `dim_dates` — dimensions
  - `fact_trending_snapshots` — daily rankings per project per date
  - `assoc_project_tags` — many-to-many project↔tag
- **Flat table** for fast queries:
  - `summarized_projects` — denormalized, one row per summarized project (PK: `name`, includes `tech_domain`)

`db_models.py` provides a SQLAlchemy ORM layer (newer, shares the same schema). Both `ProjectDatabase` classes exist and are used in different routes — be careful to understand which one you're modifying.

### Backend File Map

| File | Purpose |
|------|---------|
| `backend/app.py` | CLI entry point, 3 modes: `full` (web+scheduler), `web`, `reporter` |
| `backend/router.py` | Flask app factory, inline API routes for reports/stats/trends/projects, SPA fallback |
| `backend/routes/projects.py` | Blueprint-based projects API (pagination, search, filter, sort) |
| `backend/routes/stats.py` | Blueprint-based stats API with in-memory caching |
| `backend/app/main.py` | `job()` orchestrator — scrape → ingest → filter new → LLM summarize → save report |
| `backend/app/scraper.py` | BeautifulSoup scraper for GitHub Trending HTML |
| `backend/app/github_api.py` | GitHub REST API: repo details, README, entity info |
| `backend/app/summarizer.py` | LLM integration — uses `httpx` directly (NOT OpenAI SDK) to avoid `x-stainless-*` header issues; builds prompts, calls API with retry, extracts and cleans output |
| `backend/app/analyzer.py` | Complex SQL queries for trend dashboards (most frequent, surging stars, tag trends) |
| `backend/app/database.py` | SQLite with raw `sqlite3` — schema creation, dimension helpers, snapshots, summarized_projects CRUD |
| `backend/app/db_models.py` | SQLAlchemy ORM models + `ProjectRepository` + backward-compatible `ProjectDatabase` wrapper |
| `backend/app/cache.py` | Thread-safe in-memory `MemoryCache` with TTL, singleton via `get_cache()` |
| `backend/app/response.py` | `success_response` / `error_response` helpers + `get_pagination_params` used by Blueprint routes |
| `backend/app/notifier.py` | Multi-platform push (DingTalk markdown, Feishu card, ClawBot markdown) with HTTPS validation |
| `backend/export_static_data.py` | Exports DB + MD reports → `docs/data/*.json` for GitHub Pages static frontend |
| `backend/config/settings.py` | All env vars, prompt templates (Chinese), HTML template |
| `backend/config/logging_config.py` | Custom colored console logger with emoji levels |

### Frontend Structure

- Vue 3 + TypeScript + Vite + Tailwind CSS 3
- Vue Router with views: Home, Reports, ProjectLibrary, Rankings, TrendAnalysis, Favorites, About
- `vite.config.ts` proxies `/api` and `/images` to `localhost:5001` in dev
- Uses Chart.js for trend charts, markdown-it for report rendering
- All API calls centralized in `frontend/src/api/reports.ts`

**Dual data mode** (controlled by `VITE_STATIC_MODE`):
- `false` (dev): Fetches from live Flask API (`localhost:5001`)
- `true` (GitHub Pages): Reads from `docs/data/*.json` static files exported by `export_static_data.py`; falls back to static on connection errors even when not explicitly set

### Key Design Decisions

1. **LLM calls use raw httpx**, not OpenAI SDK — the SDK's `x-stainless-*` headers caused issues with some API proxies. The client is built in `get_llm_client()` with a hardcoded `/v1` path append.

2. **LLM output cleaning** (`strip_meta_lines`, `extract_overview_intro`, `extract_project_report`) strips `<think>` tags, XML, and meta commentary lines that some models (DeepSeek) emit. If model output format changes, check these functions.

3. **Prompts are in Chinese** and defined as constants in `config/settings.py`. The model is expected to output Markdown directly. Two prompt variants exist: `SINGLE_PROJECT_PROMPT_TEMPLATE` (full analysis) and `SINGLE_PROJECT_PROMPT_TEMPLATE_CACHE` (simpler), but only the full one is used in the current `build_project_prompt()`.

4. **Tech domain classification** (`summarizer.py`): After LLM summary, regex extracts a `**核心领域**` field and normalizes it against 14 fixed categories via keyword matching. Falls back to `'Other'`.

5. **The router has duplicate route definitions**: `backend/router.py` defines routes inline, while `backend/routes/` has Blueprint-based versions. The Blueprint versions use standardized `success_response`/`error_response` helpers and caching. Check both when modifying API behavior.

6. **GitHub Actions** (`generate-report.yml`) runs daily at UTC 00:00 (08:00 Beijing time), generates reports, exports static JSON via `export_static_data.py`, builds the Vue frontend into `docs/` with `VITE_STATIC_MODE=true`, commits+pulls+pushes back to the repo, and sends notifications.

7. **No test suite exists** in this project. There is no `tests/` directory in either backend or frontend.

## Environment Variables

**Required:** `LLM_API_KEY`, `LLM_BASE_URL`

**Optional backend:**

| Variable | Default | Purpose |
|----------|---------|---------|
| `LLM_MODEL` | `gpt-4-turbo` | LLM model name |
| `LLM_MAX_RETRIES` | `3` | LLM call retry count |
| `LLM_RETRY_DELAY` | `5` | Seconds between retries |
| `LLM_TIMEOUT` | `60` | LLM request timeout (seconds) |
| `GH_TOKEN` | — | GitHub API token (used in CI as `GH_TOKEN`, read in `settings.py`) |
| `SCHEDULE_TIME` | `08:00` | Daily run time (local server time) |
| `NUM_PROJECTS_TO_SUMMARIZE` | `8` | Max new projects to summarize per run |
| `MAX_PROJECTS_TO_SCRAPE` | `25` | Max repos to scrape from trending |
| `DAYS_TO_SKIP` | `7` | Skip projects summarized within last N days |
| `TRENDING_DATE_RANGE` | `daily` | `daily` / `weekly` / `monthly` |
| `DINGTALK_WEBHOOK` | — | DingTalk notification webhook |
| `FEISHU_WEBHOOK` | — | Feishu notification webhook |
| `CLAWBOT_WEBHOOK` | — | ClawBot notification webhook |
| `PAGES_URL` | — | GitHub Pages base URL for notification links |

**Optional frontend:**

| Variable | Default | Purpose |
|----------|---------|---------|
| `VITE_STATIC_MODE` | `false` | `true` = read from `docs/data/*.json` (GitHub Pages) |
| `VITE_API_BASE_URL` | `http://localhost:5001` | Live API base URL |

## README Maintenance

**When adding or modifying any feature, update README.md and README-EN.md in the same commit.** Sections that commonly need updating:

- `✨ 功能特性 / Features` — add or revise feature bullets
- `🏗️ 架构设计 / Architecture` — update data flow, file map, or API routes
- `⚙️ 完整环境变量 / Environment Variables` — add new env vars with defaults
- `📸 界面截图 / Screenshots` — retake screenshots if the UI changes significantly

Screenshots live in `images/screenshot_*.png`. To regenerate them, start a local static server (`python3 -m http.server 8899` from a directory where `ai-git-trending/` maps to `docs/`) and run the Playwright script at `/tmp/screenshot.mjs`.
