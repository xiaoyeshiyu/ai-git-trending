"""
Projects API routes.
"""

import os
from flask import Blueprint, jsonify, request

projects_bp = Blueprint('projects', __name__)

from app.database import ProjectDatabase
from app.response import success_response, error_response, get_pagination_params, ErrorCode
from config.logging_config import get_logger

logger = get_logger('projects', 'INFO')

db = ProjectDatabase()


def decodeURIComponent(encoded_str):
    """URL解码"""
    import urllib.parse
    try:
        return urllib.parse.unquote(encoded_str)
    except Exception:
        return encoded_str


@projects_bp.route('/project/<project_name>')
def get_project_details(project_name):
    """获取单个项目的详细信息"""
    from router import validate_project_name

    try:
        # 解码URL编码的项目名称
        decoded_project_name = decodeURIComponent(project_name)

        # 验证项目名称格式
        is_valid, error_msg = validate_project_name(decoded_project_name)
        if not is_valid:
            return error_response(ErrorCode.VALIDATION_ERROR, error_msg, 400)

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
                return success_response(project)

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
                return success_response(project)

            # 两个表都未找到，返回404错误
            logger.warning(f"项目未找到: {decoded_project_name}")
            return error_response(ErrorCode.NOT_FOUND, "Project not found", 404)
    except Exception as e:
        logger.error(f"获取项目详情错误: {e}")
        return error_response(ErrorCode.INTERNAL_ERROR, str(e), 500)


@projects_bp.route('/project', methods=['GET', 'POST'])
def get_project_details_api():
    """通过GET或POST请求获取项目详情"""
    if request.method == 'POST':
        data = request.get_json() or {}
        project_name = data.get('project_name')
    else:
        project_name = request.args.get('project_name')

    if not project_name:
        return error_response(ErrorCode.VALIDATION_ERROR, "project_name is required", 400)

    return get_project_details(project_name)


@projects_bp.route('/projects/<date>')
def get_projects_by_date(date):
    """根据日期获取项目列表"""
    try:
        from router import validate_date_string

        # 验证日期格式
        is_valid, error_msg = validate_date_string(date)
        if not is_valid:
            return error_response(ErrorCode.VALIDATION_ERROR, error_msg, 400)

        logger.info(f"获取项目列表: {date}")

        with db._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM summarized_projects WHERE summary_date = ? ORDER BY stars DESC",
                (date,)
            )
            rows = cursor.fetchall()

            if not rows:
                # 如果没有总结的项目，返回空列表
                return success_response([])

            # 获取列名
            columns = [description[0] for description in cursor.description]
            projects = [dict(zip(columns, row)) for row in rows]

            return success_response(projects)
    except Exception as e:
        logger.error(f"获取项目列表错误: {e}")
        return error_response(ErrorCode.INTERNAL_ERROR, str(e), 500)


@projects_bp.route('/projects')
def get_projects():
    """获取项目列表（支持分页、排序、筛选、搜索）"""
    try:
        # 获取分页参数
        page, page_size = get_pagination_params(request)

        # 获取排序参数
        sort_by = request.args.get('sort_by', 'stars')
        order = request.args.get('order', 'desc')

        # 验证排序字段
        allowed_sort_fields = ['stars', 'forks', 'contributor_count', 'name', 'summary_date', 'score']
        if sort_by not in allowed_sort_fields:
            sort_by = 'stars'

        # 验证排序方向
        if order not in ['asc', 'desc']:
            order = 'desc'

        # 获取筛选参数
        language_filter = request.args.get('language')
        tech_domain_filter = request.args.get('tech_domain')
        min_stars = request.args.get('min_stars', type=int)
        max_stars = request.args.get('max_stars', type=int)
        min_score = request.args.get('min_score', type=int)
        max_score = request.args.get('max_score', type=int)
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        search = request.args.get('search')

        with db._get_connection() as conn:
            cursor = conn.cursor()

            # 构建查询
            base_query = "FROM summarized_projects WHERE 1=1"
            params = []

            if language_filter:
                base_query += " AND language = ?"
                params.append(language_filter)

            # 技术领域筛选
            if tech_domain_filter:
                base_query += " AND tech_domain = ?"
                params.append(tech_domain_filter)

            if min_stars is not None:
                base_query += " AND stars >= ?"
                params.append(min_stars)

            if max_stars is not None:
                base_query += " AND stars <= ?"
                params.append(max_stars)

            # 日期范围筛选
            if date_from:
                base_query += " AND summary_date >= ?"
                params.append(date_from)

            if date_to:
                base_query += " AND summary_date <= ?"
                params.append(date_to)

            # 关键词搜索（搜索项目名和描述）
            if search:
                base_query += " AND (name LIKE ? OR description LIKE ?)"
                search_pattern = f"%{search}%"
                params.extend([search_pattern, search_pattern])

            # 获取总数
            count_query = f"SELECT COUNT(*) {base_query}"
            cursor.execute(count_query, params)
            total = cursor.fetchone()[0] or 0

            # 排序和分页 - 使用安全映射防止 SQL 注入
            ORDER_MAPPING = {
                'stars': 'stars',
                'forks': 'forks',
                'contributor_count': 'contributor_count',
                'name': 'name',
                'summary_date': 'summary_date',
                'score': 'score'
            }
            safe_sort = ORDER_MAPPING.get(sort_by, 'stars')
            safe_order = 'DESC' if order == 'desc' else 'ASC'

            # 获取分页数据
            offset = (page - 1) * page_size
            data_query = f"SELECT * {base_query} ORDER BY {safe_sort} {safe_order} LIMIT ? OFFSET ?"
            query_params = params + [page_size, offset]

            cursor.execute(data_query, query_params)
            rows = cursor.fetchall()

            # 获取列名
            columns = [description[0] for description in cursor.description]
            projects = [dict(zip(columns, row)) for row in rows]

            # 返回分页响应
            response_data = {
                "items": projects,
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": (total + page_size - 1) // page_size
            }

            return success_response(response_data)
    except Exception as e:
        logger.error(f"获取项目列表错误: {e}")
        return error_response(ErrorCode.INTERNAL_ERROR, str(e), 500)
