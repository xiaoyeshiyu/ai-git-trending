# GitHub Trending Reporter 🚀

English | [简体中文](./README.md)

**Automatically tracks GitHub Trending, uses LLM to deeply analyze popular open-source projects daily, generates Chinese insight reports, and presents tech trends through an interactive web dashboard.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Backend-Flask-green.svg)](https://flask.palletsprojects.com/)
[![Vue 3](https://img.shields.io/badge/Frontend-Vue%203-42b883.svg)](https://vuejs.org/)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)

---

## ✨ Features

- **📈 Daily Automated Analysis**: Scrapes GitHub Trending and generates Chinese insight reports (one-sentence review, tech highlights, potential impact) via LLM
- **🤖 Zero-Server Operation**: GitHub Actions runs daily at 08:00 Beijing time, commits reports back to the repo, and deploys to GitHub Pages
- **🖥️ Intelligence Terminal UI**: Dark-themed dashboard showing real-time stats, latest report summary, and a project sidebar
- **📊 Multi-dimensional Trend Analysis**: Most frequently trending projects, star growth rankings, language distribution charts, tech domain classification
- **🏆 Project Leaderboard**: Full project ranking by stars, filterable by time period and tech domain
- **📁 Report Archive**: All daily reports with Markdown / HTML dual-format download
- **⭐ Favorites**: Locally persisted project bookmarks
- **🔧 Highly Configurable**: LLM model, API endpoint, scrape count, notification channels — all via environment variables

## 📸 Screenshots

| Page | Screenshot |
|------|------------|
| **Intelligence Terminal** — live stats + latest report summary | ![Home](images/screenshot_home.png) |
| **Trend** — most frequent projects / fastest star growth | ![Trend](images/screenshot_trend.png) |
| **Rankings** — full project star leaderboard + report archive | ![Rankings](images/screenshot_rankings.png) |
| **Trend Analysis** — language distribution + tech domain charts | ![Analysis](images/screenshot_analysis.png) |

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, Flask, SQLite, httpx |
| Frontend | Vue 3, TypeScript, Vite, Tailwind CSS 3, Chart.js |
| Automation | GitHub Actions, `schedule` library |
| Deployment | Docker, GitHub Pages |

## 🏗️ Architecture

### Backend

```
GitHub Trending HTML
        │
        ▼
   scraper.py          ← BeautifulSoup scrapes trending repo list
        │
        ├──► database.py     ← writes fact_trending_snapshots (star schema)
        │
        └──► filter already-analyzed projects
                │
                ▼
         summarizer.py       ← httpx direct LLM call (not OpenAI SDK)
                │             builds Chinese prompt → parses Markdown output
                ▼
          database.py        ← writes summarized_projects (flat fast-query table)
                │
                ▼
         file_writer.py      ← generates output/md/ and output/html/ reports
                │
                ▼
          notifier.py        ← pushes to DingTalk / Feishu / ClawBot
```

**API Layer** (Flask):

| Module | Description |
|--------|-------------|
| `router.py` | Inline routes: `/api/reports`, `/api/trending`, `/api/trends`, `/api/stats`, etc. |
| `routes/projects.py` | Blueprint: project pagination / search / filter |
| `routes/stats.py` | Blueprint: stats data (5-min in-memory cache) |

**Database** (SQLite at `output/reporter.db`):

- Star schema: `dim_projects`, `dim_languages`, `dim_dates`, `fact_trending_snapshots`
- Flat table: `summarized_projects` (includes `tech_domain`, `analysis` for fast frontend queries)

### Frontend

```
frontend/src/
├── views/
│   ├── Home.vue          ← Intelligence terminal: stats + latest report + project sidebar
│   ├── Trend.vue         ← Trend: most frequent / fastest rising (7d/30d)
│   ├── Rankings.vue      ← Rankings: star leaderboard + report archive
│   ├── TrendAnalysis.vue ← Trend analysis: language + domain charts (Chart.js)
│   ├── Favorites.vue     ← Favorites (localStorage persistence)
│   └── Reports.vue       ← Daily report list
├── components/
│   ├── ProjectCard.vue   ← Project card component
│   ├── ProjectModal.vue  ← Project detail modal
│   ├── ReportModal.vue   ← Report reader modal (markdown-it rendering)
│   └── StatsChart.vue    ← Statistics charts
└── api/reports.ts        ← Unified API layer (dual-mode: Live API / Static JSON)
```

**Dual Data Mode** (controlled by `VITE_STATIC_MODE`):

- `false` (local dev): requests Flask backend at `localhost:5001`
- `true` (GitHub Pages): reads `docs/data/*.json` static files, auto-falls back when backend is unreachable

## 🚀 Quick Start

### Option 1: GitHub Actions Automation (Recommended — no server needed)

**1. Fork / clone the repository**

**2. Configure Secrets** (`Settings → Secrets and variables → Actions`)

| Secret | Required | Description |
|--------|----------|-------------|
| `LLM_API_KEY` | ✅ Yes | LLM API key |
| `LLM_BASE_URL` | ✅ Yes | LLM API base URL (OpenAI-compatible) |
| `LLM_MODEL` | Optional | Model name, default `gpt-4-turbo` |
| `GH_TOKEN` | Optional | GitHub Token to increase API rate limits |
| `DINGTALK_WEBHOOK` | Optional | DingTalk notification webhook |
| `FEISHU_WEBHOOK` | Optional | Feishu notification webhook |
| `CLAWBOT_WEBHOOK` | Optional | ClawBot notification webhook |

**3. Configure Variables** (optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `NUM_PROJECTS_TO_SUMMARIZE` | `8` | New projects to analyze per day |
| `MAX_PROJECTS_TO_SCRAPE` | `25` | Total projects scraped from Trending |
| `PAGES_URL` | — | GitHub Pages URL for notification links |

**4. Trigger first run manually**

`Actions → Generate GitHub Trending Report → Run workflow`

**5. Enable GitHub Pages**

`Settings → Pages → Source: Deploy from a branch → Branch: main / docs`

---

### Option 2: Docker Deployment (with Web Dashboard)

```bash
docker build -t git-trending:latest .
docker run -d \
  --name git-trending \
  -p 5001:5001 \
  -v $(pwd)/output:/app/output \
  -e LLM_API_KEY="sk-xxx" \
  -e LLM_BASE_URL="https://api.openai.com/v1" \
  git-trending:latest
```

Visit `http://localhost:5001`

---

### Option 3: Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env   # fill in LLM_API_KEY and LLM_BASE_URL
python app.py --mode web --debug

# Frontend (new terminal)
cd frontend
npm install
npm run dev            # http://localhost:5173, proxies /api → :5001
```

## ⚙️ Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_API_KEY` | — | **Required** |
| `LLM_BASE_URL` | — | **Required** |
| `LLM_MODEL` | `gpt-4-turbo` | LLM model name |
| `LLM_MAX_RETRIES` | `3` | LLM call retry count |
| `LLM_RETRY_DELAY` | `5` | Seconds between retries |
| `LLM_TIMEOUT` | `60` | Request timeout (seconds) |
| `GH_TOKEN` | — | GitHub API Token |
| `SCHEDULE_TIME` | `08:00` | Daily execution time (server local time) |
| `NUM_PROJECTS_TO_SUMMARIZE` | `8` | New projects to analyze per run |
| `MAX_PROJECTS_TO_SCRAPE` | `25` | Total projects scraped per run |
| `DAYS_TO_SKIP` | `7` | Skip projects analyzed within last N days |
| `TRENDING_DATE_RANGE` | `daily` | `daily` / `weekly` / `monthly` |
| `DINGTALK_WEBHOOK` | — | DingTalk notification |
| `FEISHU_WEBHOOK` | — | Feishu notification |
| `CLAWBOT_WEBHOOK` | — | ClawBot notification |
| `PAGES_URL` | — | GitHub Pages URL (for notifications) |

## 📁 Output Directory

```
output/
├── reporter.db          # SQLite database (historical data)
├── md/                  # Markdown daily reports
└── html/                # HTML daily reports
```

## 🤝 Contributing

Issues and Pull Requests are welcome.

> **Convention**: When adding or modifying features, please update the relevant sections of this README (Features, Architecture, Environment Variables, etc.) to keep documentation in sync with code.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
