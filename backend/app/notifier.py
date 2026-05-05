"""多平台消息推送通知模块：钉钉、飞书、ClawBot"""

import json
import os
import urllib.request
from config.logging_config import get_logger

logger = get_logger('notifier', 'INFO')


def _validate_webhook_url(url: str) -> bool:
    """确保 webhook 使用 HTTPS"""
    if not url.startswith('https://'):
        logger.warning(f"Webhook URL must use HTTPS, got: {url[:50]}...")
        return False
    return True


def _post_json(url: str, payload: dict) -> bool:
    """发送 JSON POST 请求到 webhook URL"""
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode()
            logger.info(f"Webhook response ({resp.status}): {body[:200]}")
            return resp.status == 200
    except Exception as e:
        logger.error(f"Webhook request failed: {e}")
        return False


def send_dingtalk(webhook: str, title: str, text: str) -> bool:
    """钉钉机器人：Markdown 消息"""
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": text
        }
    }
    return _post_json(webhook, payload)


def send_feishu(webhook: str, title: str, text: str) -> bool:
    """飞书机器人：富文本卡片消息"""
    payload = {
        "msgtype": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": title},
                "template": "blue"
            },
            "elements": [
                {"tag": "markdown", "content": text},
                {"tag": "hr"},
                {"tag": "note", "elements": [{"tag": "plain_text", "content": "GitHub Trending Reporter · 每日自动推送"}]}
            ]
        }
    }
    return _post_json(webhook, payload)


def send_clawbot(webhook: str, title: str, text: str) -> bool:
    """ClawBot 框架：Markdown 消息"""
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": f"## {title}\n\n{text}"
        }
    }
    return _post_json(webhook, payload)


def notify_all(title: str, text: str) -> dict:
    """向所有配置了 webhook 的平台发送通知，返回各平台结果"""
    results = {}

    webhook = os.getenv('DINGTALK_WEBHOOK', '')
    if webhook and _validate_webhook_url(webhook):
        ok = send_dingtalk(webhook, title, text)
        results['dingtalk'] = 'ok' if ok else 'failed'
        logger.info(f"📢 DingTalk: {'sent' if ok else 'failed'}")
    elif webhook:
        results['dingtalk'] = 'skipped (invalid url)'

    webhook = os.getenv('FEISHU_WEBHOOK', '')
    if webhook and _validate_webhook_url(webhook):
        ok = send_feishu(webhook, title, text)
        results['feishu'] = 'ok' if ok else 'failed'
        logger.info(f"📢 Feishu: {'sent' if ok else 'failed'}")
    elif webhook:
        results['feishu'] = 'skipped (invalid url)'

    webhook = os.getenv('CLAWBOT_WEBHOOK', '')
    if webhook and _validate_webhook_url(webhook):
        ok = send_clawbot(webhook, title, text)
        results['clawbot'] = 'ok' if ok else 'failed'
        logger.info(f"📢 ClawBot: {'sent' if ok else 'failed'}")
    elif webhook:
        results['clawbot'] = 'skipped (invalid url)'

    return results


def build_notification_text(latest_md_path: str, pages_url: str = '') -> tuple:
    """从最新报告中提取标题和摘要文本"""
    try:
        with open(latest_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (FileNotFoundError, PermissionError, OSError) as e:
        logger.error(f"Failed to read report for notification: {e}")
        return "GitHub Trending 日报", "今日报告生成完成，请查看 Pages 页面。"

    title = "GitHub Trending 日报"
    overview_lines = []
    in_overview = False

    for line in content.split('\n'):
        if line.startswith('## 今日热点'):
            in_overview = True
            continue
        if in_overview:
            if line.startswith('## ') or line.startswith('### ✨'):
                break
            stripped = line.strip()
            if stripped:
                overview_lines.append(stripped)

    overview = '\n'.join(overview_lines[:5]) if overview_lines else content[:500]

    text = overview
    if pages_url:
        text += f'\n\n[查看完整报告]({pages_url})'

    return title, text
