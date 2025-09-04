from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from config.settings import MD_DIR, HTML_DIR
from config.logging_config import get_logger
import os
from datetime import datetime, timedelta
from app.database import ProjectDatabase
import urllib.parse

# 创建日志记录器
logger = get_logger('router', 'INFO')

app = Flask(__name__, static_folder='../images', static_url_path='/images')
CORS(app)  # 启用CORS支持
db = ProjectDatabase()

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
            "project_count": project_count if project_count > 0 else 4
        }
        
        return jsonify(report)
    except Exception as e:
        logger.error(f"Error in /api/report/{date_str}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/download/<date_str>/<format>')
def download_report(date_str, format):
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

@app.route('/api/stats')
def get_stats():
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM summarized_projects")
            total_projects = cursor.fetchone()[0]

            cursor.execute("SELECT language, COUNT(*) as count FROM summarized_projects WHERE language != 'N/A' AND language IS NOT NULL GROUP BY language ORDER BY count DESC LIMIT 1")
            top_lang_row = cursor.fetchone()
            top_language = top_lang_row[0] if top_lang_row else "N/A"

            one_week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            cursor.execute("SELECT COUNT(*) FROM summarized_projects WHERE summary_date >= ?", (one_week_ago,))
            weekly_new = cursor.fetchone()[0]
            
            total_reports = len([f for f in os.listdir(MD_DIR) if f.endswith('.md')])

            # New Stats
            cursor.execute("SELECT SUM(forks) FROM summarized_projects")
            total_forks = cursor.fetchone()[0] or 0

            cursor.execute("SELECT AVG(contributor_count) FROM summarized_projects WHERE contributor_count != 'N/A'")
            avg_contributors = cursor.fetchone()[0] or 0
            
            # 计算活跃度分数 - 基于贡献者数量、stars和forks等指标
            cursor.execute("SELECT AVG(contributor_count) FROM summarized_projects WHERE contributor_count != 'N/A'")
            avg_contributors = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT AVG(stars) FROM summarized_projects")
            avg_stars = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT AVG(forks) FROM summarized_projects")
            avg_forks = cursor.fetchone()[0] or 0
            
            # 简单的活跃度计算公式
            # 假设有一个基准值，然后根据实际数据进行归一化计算
            base_contributors = 10
            base_stars = 100
            base_forks = 50
            
            # 计算各项指标的归一化值（0-100）
            contributors_score = min(100, (avg_contributors / base_contributors) * 25)
            stars_score = min(100, (avg_stars / base_stars) * 40)
            forks_score = min(100, (avg_forks / base_forks) * 35)
            
            # 综合计算活跃度分数
            activity_score = round(contributors_score + stars_score + forks_score)
            
            # 确保活跃度分数在合理范围内
            activity_score = max(0, min(100, activity_score))
            
            stats = {
                "totalReports": total_reports,
                "totalProjects": total_projects,
                "topLanguage": top_language,
                "weeklyNew": weekly_new,
                "totalForks": f"{total_forks:,}", # Formatted with commas
                "avgContributors": round(avg_contributors, 1),
                "activityScore": activity_score
            }
            return jsonify(stats)
    except Exception as e:
        logger.error(f"Error in /api/stats: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/language-distribution')
def get_language_distribution():
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            
            # 获取语言分布数据
            cursor.execute("SELECT language, COUNT(*) as count FROM summarized_projects WHERE language != 'N/A' AND language IS NOT NULL GROUP BY language ORDER BY count DESC LIMIT 10")
            language_rows = cursor.fetchall()
            
            # 计算总项目数（排除N/A语言）
            cursor.execute("SELECT COUNT(*) FROM summarized_projects WHERE language != 'N/A' AND language IS NOT NULL")
            total_valid_projects = cursor.fetchone()[0] or 1  # 避免除以零
            
            # 格式化语言分布数据
            language_distribution = []
            for language, count in language_rows:
                percentage = round((count / total_valid_projects) * 100)
                # 为每种语言分配一个颜色类
                color_classes = {
                    'JavaScript': 'bg-gradient-to-r from-yellow-500 to-yellow-600',
                    'Python': 'bg-gradient-to-r from-green-500 to-green-600',
                    'TypeScript': 'bg-gradient-to-r from-blue-500 to-blue-600',
                    'Go': 'bg-gradient-to-r from-cyan-500 to-cyan-600',
                    'Rust': 'bg-gradient-to-r from-orange-500 to-orange-600',
                    'Java': 'bg-gradient-to-r from-red-500 to-red-600',
                    'C++': 'bg-gradient-to-r from-blue-500 to-blue-600',
                    'C#': 'bg-gradient-to-r from-purple-500 to-purple-600',
                    'PHP': 'bg-gradient-to-r from-blue-500 to-blue-600',
                    'Ruby': 'bg-gradient-to-r from-red-500 to-red-600'
                }
                color_class = color_classes.get(language, 'bg-gradient-to-r from-gray-500 to-gray-600')
                
                language_distribution.append({
                    "name": language,
                    "count": count,
                    "percentage": percentage,
                    "colorClass": color_class
                })
            
            return jsonify(language_distribution)
    except Exception as e:
        logger.error(f"Error in /api/language-distribution: {e}")
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

@app.route('/api/project/<project_name>')
def get_project_details(project_name):
    """获取单个项目的详细信息"""
    try:
        # 解码URL编码的项目名称
        decoded_project_name = decodeURIComponent(project_name)
        logger.info(f"获取项目详情: {decoded_project_name}")
        
        with db._get_connection() as conn:
            cursor = conn.cursor()
            
            # 首先在summarized_projects表中查询
            cursor.execute(
                "SELECT name, url, description, language, stars, forks, contributor_count, created_at, updated_at, open_issues, watchers, summary_date FROM summarized_projects WHERE name = ?",
                (decoded_project_name,)
            )
            row = cursor.fetchone()
            
            if row:
                # 找到项目，返回详细信息
                project = {
                    "name": row[0],
                    "url": row[1],
                    "description": row[2],
                    "language": row[3],
                    "stars": row[4],
                    "forks": row[5],
                    "contributor_count": row[6],
                    "created_at": row[7],
                    "updated_at": row[8],
                    "open_issues": row[9],
                    "watchers": row[10],
                    "summary_date": row[11]
                }
                return jsonify(project)
            
            # 如果在summarized_projects表中未找到，尝试在dim_projects表中查询基本信息
            cursor.execute(
                "SELECT p.name, p.url, p.description, l.name as language FROM dim_projects p LEFT JOIN dim_languages l ON p.language_id = l.language_id WHERE p.name = ?",
                (decoded_project_name,)
            )
            row = cursor.fetchone()
            
            if row:
                # 找到基本项目信息，返回基本信息
                project = {
                    "name": row[0],
                    "url": row[1],
                    "description": row[2],
                    "language": row[3] or "Unknown",
                    "stars": 0,
                    "forks": 0,
                    "contributor_count": 0,
                    "created_at": "N/A",
                    "updated_at": "N/A",
                    "open_issues": 0,
                    "watchers": 0,
                    "summary_date": "N/A",
                    "message": "此项目尚未被总结，只返回基本信息"
                }
                return jsonify(project)
            
            # 两个表都未找到，返回404错误
            logger.warning(f"项目未找到: {decoded_project_name}")
            return jsonify({"error": "Project not found", "project_name": decoded_project_name}), 404
    except Exception as e:
        logger.error(f"获取项目详情错误: {e}")
        return jsonify({"error": str(e), "project_name": project_name}), 500

@app.route('/api/project', methods=['POST'])
def get_project_details_post():
    """通过POST请求获取单个项目的详细信息，参数放在请求体中"""
    try:
        # 从请求体中获取项目名称
        data = request.get_json()
        if not data or 'project_name' not in data:
            logger.warning("POST请求缺少project_name参数")
            return jsonify({"error": "Missing project_name parameter in request body"}), 400
        
        project_name = data['project_name']
        logger.info(f"通过POST请求获取项目详情: {project_name}")
        
        with db._get_connection() as conn:
            cursor = conn.cursor()
            
            # 首先在summarized_projects表中查询
            cursor.execute(
                "SELECT name, url, description, language, stars, forks, contributor_count, created_at, updated_at, open_issues, watchers, summary_date FROM summarized_projects WHERE name = ?",
                (project_name,)
            )
            row = cursor.fetchone()
            
            if row:
                # 找到项目，返回详细信息
                project = {
                    "name": row[0],
                    "url": row[1],
                    "description": row[2],
                    "language": row[3],
                    "stars": row[4],
                    "forks": row[5],
                    "contributor_count": row[6],
                    "created_at": row[7],
                    "updated_at": row[8],
                    "open_issues": row[9],
                    "watchers": row[10],
                    "summary_date": row[11]
                }
                return jsonify(project)
            
            # 如果在summarized_projects表中未找到，尝试在dim_projects表中查询基本信息
            cursor.execute(
                "SELECT p.name, p.url, p.description, l.name as language FROM dim_projects p LEFT JOIN dim_languages l ON p.language_id = l.language_id WHERE p.name = ?",
                (project_name,)
            )
            row = cursor.fetchone()
            
            if row:
                # 找到基本项目信息，返回基本信息
                project = {
                    "name": row[0],
                    "url": row[1],
                    "description": row[2],
                    "language": row[3] or "Unknown",
                    "stars": 0,
                    "forks": 0,
                    "contributor_count": 0,
                    "created_at": "N/A",
                    "updated_at": "N/A",
                    "open_issues": 0,
                    "watchers": 0,
                    "summary_date": "N/A",
                    "message": "此项目尚未被总结，只返回基本信息"
                }
                return jsonify(project)
            
            # 两个表都未找到，返回404错误
            logger.warning(f"项目未找到: {project_name}")
            return jsonify({"error": "Project not found", "project_name": project_name}), 404
    except Exception as e:
        logger.error(f"通过POST请求获取项目详情错误: {e}")
        return jsonify({"error": str(e), "project_name": project_name if 'project_name' in locals() else "N/A"}), 500

# 辅助函数：解码URI组件
def decodeURIComponent(encoded_str):
    """解码URI编码的字符串，适配前端encodeURIComponent的编码"""
    return urllib.parse.unquote(encoded_str)
