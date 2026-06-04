"""统一的 API 响应格式"""

from flask import jsonify
from enum import Enum


class ErrorCode(Enum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    INTERNAL_ERROR = "INTERNAL_ERROR"


def success_response(data, meta=None):
    body = {"success": True, "data": data}
    if meta:
        body["meta"] = meta
    return jsonify(body)


def error_response(code: ErrorCode, message: str, status_code: int = 400):
    return jsonify({"success": False, "error": {"code": code.value, "message": message}}), status_code


def get_pagination_params(request):
    try:
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 20))
    except (ValueError, TypeError):
        page, page_size = 1, 20
    page = max(1, page)
    page_size = min(100, max(1, page_size))
    return page, page_size
