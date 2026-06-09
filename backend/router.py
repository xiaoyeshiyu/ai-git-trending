from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from config.settings import MD_DIR, HTML_DIR
from config.logging_config import get_logger
import os
from datetime import datetime, timedelta
from app.database import ProjectDatabase
import threading

# 创建日志记录器
logger = get_logger('router', 'INFO')

# Trending data cache (8-hour TTL) — in-memory, lives only inside this process
_TRENDING_CACHE_TTL_SECONDS = 8 * 60 * 60
_trending_cache = {"data": None, "expires_at": 0}
_trending_cache_lock = threading.Lock()

app = Flask(__name__, static_folder='../images', static_url_path='/images')
CORS(app)  # 启用CORS支持
db = ProjectDatabase()

# Register blueprints
from routes.projects import projects_bp
from routes.stats import stats_bp
app.register_blueprint(projects_bp, url_prefix='/api')
app.register_blueprint(stats_bp, url_prefix='/api')

def get_report_data_from_filename(filename):
    try:
        date_str = filename.split('_')[-1].replace('.md', '')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return {
            "isoDate": date_str,
            "displayDate": date_obj.strftime('%Y年%m月%d日'),
            "weekday": date_obj.strftime('%A'),
            "path": os.path.join(MD_DIR, filename)
        }
    except (IndexError, ValueError):
        return None

@app.route('/api/reports')
def get_reports():
    try:
        files = os.listdir(MD_DIR)
        md_files = sorted([f for f in files if f.endswith('.md')], reverse=True)
        
        reports = []
        for filename in md_files:
            data = get_report_data_from_filename(filename)
            if data:
                with open(data['path'], 'r', encoding='utf-8') as f:
                    content = f.read()
                    project_count = content.count('### ✨')
                
                report = {
                    "date": data['isoDate'],
                    "project_count": project_count if project_count > 0 else 4
                }
                reports.append(report)

        return jsonify(reports)
    except Exception as e:
        logger.error(f"Error in /api/reports: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/report/<date_str>')
def get_report_content(date_str):
    is_valid, error_msg = validate_date_string(date_str)
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    filename = f"github_trending_{date_str}.md"
    filepath = os.path.join(MD_DIR, filename)

    if not os.path.exists(filepath):
        logger.warning(f"Report not found: {filepath}")
        return jsonify({"error": "Report not found"}), 404

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        project_count = content.count('### ✨')
        
        report = {
            "date": date_str,
            "content": content,
            "project_count": project_count if project_count > 0 else 0
        }
        
        return jsonify(report)
    except Exception as e:
        logger.error(f"Error in /api/report/{date_str}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/download/<date_str>/<format>')
def download_report(date_str, format):
    is_valid, error_msg = validate_date_string(date_str)
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    if format not in ['html', 'md']:
        return jsonify({"error": "Invalid format specified"}), 400

    dir_path = HTML_DIR if format == 'html' else MD_DIR
    filename = f"github_trending_{date_str}.{format}"
    
    if not os.path.exists(os.path.join(dir_path, filename)):
        logger.warning(f"Download request for non-existent file: {filename}")
        return jsonify({"error": "File not found"}), 404

    try:
        return send_from_directory(dir_path, filename, as_attachment=True)
    except Exception as e:
        logger.error(f"Error downloading file {filename}: {e}")
        return jsonify({"error": "Could not process file download"}), 500

@app.route('/api/trending')
def get_trending():
    """Return live trending repositories with 8-hour caching.

    Developer scraping was dropped — the frontend only consumes `repositories`,
    and scraping developers roughly doubled the cold-cache response time (~30s),
    causing the request to exceed the client timeout.
    """
    import time
    now = time.time()
    with _trending_cache_lock:
        if _trending_cache["data"] is not None and now < _trending_cache["expires_at"]:
            logger.info("📦 Returning cached trending data")
            return jsonify(_trending_cache["data"])

    try:
        from app.scraper import scrape_github_trending

        repos = scrape_github_trending() or []

        data = {
            "repositories": repos,
            "developers": [],
            "updated_at": datetime.now().isoformat(),
        }

        with _trending_cache_lock:
            _trending_cache["data"] = data
            _trending_cache["expires_at"] = now + _TRENDING_CACHE_TTL_SECONDS

        return jsonify(data)
    except Exception as e:
        logger.error(f"Error in /api/trending: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/trends')
def get_trends_data():
    try:
        # Get 'days' from query parameters, default to 7
        days_str = request.args.get('days', '7')
        try:
            days = int(days_str)
            # Add some validation, e.g., allow only specific values
            allowed_days = [7, 30, 182, 365]
            if days not in allowed_days:
                # Or just cap it, for now let's stick to allowed values for simplicity
                days = 7
        except ValueError:
            days = 7

        # Import here to avoid circular imports
        from app.analyzer import analyze_trends

        logger.info(f"📊 Received trends request for {days} days.")
        trends_data = analyze_trends(days=days)
        return jsonify(trends_data)
    except Exception as e:
        logger.error(f"Error in /api/trends: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/trend-data')
def get_trend_data():
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            
            # 获取总项目数
            cursor.execute("SELECT COUNT(*) FROM summarized_projects")
            total_projects = cursor.fetchone()[0] or 0
            
            # 获取本周新增项目数
            one_week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            cursor.execute("SELECT COUNT(*) FROM summarized_projects WHERE summary_date >= ?", (one_week_ago,))
            weekly_new = cursor.fetchone()[0] or 0
            
            # 获取活跃项目数（过去一周有更新的项目）
            one_week_ago_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            cursor.execute("SELECT COUNT(*) FROM summarized_projects WHERE updated_at >= ?", (one_week_ago_date,))
            active_projects = cursor.fetchone()[0] or 0
            
            # 获取热门项目数（stars > 1000）
            cursor.execute("SELECT COUNT(*) FROM summarized_projects WHERE stars > 1000")
            popular_projects = cursor.fetchone()[0] or 0
            
            # 获取趋势项目数（最近获得较多stars的项目）
            # 这里简化处理，实际应根据趋势计算
            trend_projects = max(0, int(total_projects * 0.05))
            
            # 计算变化趋势（这里简化处理）
            trend_data = [
                {"label": "新项目", "value": weekly_new, "change": 1, "colorClass": "bg-green-400"},
                {"label": "活跃项目", "value": active_projects, "change": 1, "colorClass": "bg-blue-400"},
                {"label": "热门项目", "value": popular_projects, "change": 0, "colorClass": "bg-purple-400"},
                {"label": "趋势项目", "value": trend_projects, "change": -1, "colorClass": "bg-pink-400"}
            ]
            
            return jsonify(trend_data)
    except Exception as e:
        logger.error(f"Error in /api/trend-data: {e}")
        return jsonify({"error": str(e)}), 500

# Frontend static file serving (for Docker / production)
FRONTEND_DIST = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist')


@app.route('/')
def serve_index():
    if os.path.isfile(os.path.join(FRONTEND_DIST, 'index.html')):
        return send_from_directory(FRONTEND_DIST, 'index.html')
    return jsonify({"error": "Frontend not built"}), 404


@app.route('/<path:path>')
def serve_frontend(path):
    # API and image routes are already handled by specific routes above
    if path.startswith('api/') or path.startswith('images/'):
        return jsonify({"error": "Not found"}), 404

    file_path = os.path.join(FRONTEND_DIST, path)
    if os.path.isfile(file_path):
        return send_from_directory(FRONTEND_DIST, path)

    # SPA fallback: serve index.html for all other paths
    if os.path.isfile(os.path.join(FRONTEND_DIST, 'index.html')):
        return send_from_directory(FRONTEND_DIST, 'index.html')

    return jsonify({"error": "Not found"}), 404


def validate_project_name(name: str) -> tuple:
    """验证项目名称格式为 owner/repo"""
    if not name or '/' not in name:
        return False, "Project name must be in 'owner/repo' format"
    parts = name.split('/')
    if len(parts) != 2 or not parts[0] or not parts[1]:
        return False, "Project name must be in 'owner/repo' format"
    return True, ""


def validate_date_string(date_str: str) -> tuple:
    """验证日期字符串格式为 YYYY-MM-DD"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True, ""
    except (ValueError, TypeError):
        return False, "Date must be in YYYY-MM-DD format"
