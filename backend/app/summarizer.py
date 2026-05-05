from collections import Counter
import re
import time

from openai import OpenAI

from config.logging_config import get_logger
from config.settings import (
    LLM_API_KEY,
    LLM_BASE_URL,
    LLM_MAX_RETRIES,
    LLM_MODEL,
    LLM_RETRY_DELAY,
    LLM_TIMEOUT,
)
from .github_api import get_entity_details, get_entity_repos

logger = get_logger('summarizer', 'INFO')

# 固定的技术领域分类
TECH_DOMAINS = [
    'AI/ML',          # 人工智能/机器学习
    'LLM Apps',       # 大模型应用
    'Web',            # Web开发
    'Frontend',       # 前端框架
    'Mobile',         # 移动开发
    'DevOps',         # DevOps/云原生
    'Data Science',   # 数据科学
    'Database',       # 数据库
    'Tools',          # API/工具库
    'Security',       # 安全
    'Blockchain',     # 区块链
    'Gaming',         # 游戏开发
    'OS',             # 操作系统/系统编程
    'IoT',            # 物联网
    'Other'           # 其他
]

# 领域关键词映射
DOMAIN_KEYWORDS = {
    'AI/ML': ['人工智能', 'AI', '机器学习', 'ML', '深度学习', '神经网络', 'LLM', '大模型', 'GPT', 'transformer', '模型训练', '算法'],
    'LLM Apps': ['ChatGPT', 'Claude', 'GPT', 'LLM', '大语言模型', '对话', '聊天机器人', 'AI应用', 'AIGC', '生成式AI', 'RAG', '向量数据库'],
    'Web': ['Web', '后端', 'API', 'REST', 'GraphQL', '服务端', '网站', 'HTTP', '服务器'],
    'Frontend': ['前端', 'React', 'Vue', 'Angular', 'Svelte', 'UI', '组件库', 'CSS', 'JavaScript', 'TypeScript', 'DOM', '样式'],
    'Mobile': ['移动', 'iOS', 'Android', 'Flutter', 'React Native', 'Swift', 'Kotlin', 'App', '小程序'],
    'DevOps': ['DevOps', 'Docker', 'Kubernetes', 'K8S', 'CI/CD', '云原生', '容器', '自动化', '部署', 'Pipeline', 'Terraform'],
    'Data Science': ['数据科学', '数据分析', '数据处理', 'Pandas', 'NumPy', '可视化', 'Jupyter', ' Notebook', '统计', '挖掘'],
    'Database': ['数据库', 'DB', 'SQL', 'NoSQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', '存储', 'ORM'],
    'Tools': ['工具', 'CLI', '命令行', '工具库', 'SDK', '开发工具', '效率', '脚本', '自动化工具'],
    'Security': ['安全', 'Security', '加密', 'Auth', 'OAuth', 'JWT', '权限', '隐私', '漏洞', '渗透'],
    'Blockchain': ['区块链', 'Blockchain', 'Web3', '以太坊', 'Solidity', '智能合约', 'Crypto', 'NFT', 'DeFi'],
    'Gaming': ['游戏', 'Game', 'Unity', 'Unreal', '3D', 'VR', 'AR', '引擎'],
    'OS': ['操作系统', 'Kernel', '系统编程', 'Rust', 'C/C++', '嵌入式', '驱动', '硬件', '底层'],
    'IoT': ['物联网', 'IoT', '传感器', '嵌入式', '硬件', 'Arduino', '树莓派', 'MCU']
}


def normalize_tech_domain(domain_text: str) -> str:
    """将LLM输出的技术领域标准化为固定分类"""
    if not domain_text:
        return 'Other'

    domain_text = domain_text.strip().lower()

    # 精确匹配
    for domain in TECH_DOMAINS:
        if domain_text == domain.lower():
            return domain

    # 关键词匹配
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in domain_text:
                return domain

    return 'Other'


def extract_tech_domain(content: str) -> str:
    """从LLM输出中提取技术领域"""
    if not content:
        return 'Other'

    # 匹配 **核心领域**：xxx 格式
    match = re.search(r'\*\*核心领域\*\*[:：]\s*(.+)', content)
    if match:
        domain_text = match.group(1).strip()
        return normalize_tech_domain(domain_text)

    return 'Other'


OVERVIEW_HEADING_PATTERN = re.compile(r"(?m)^##\s+.+$")
PROJECT_HEADING_PATTERN = re.compile(r"(?m)^#\s+.+$")
ENTITY_LINE_PATTERNS = (
    re.compile(r"(?m)^\*\*技术影响力\*\*[:：]\s*.+$"),
    re.compile(r"(?m)^\*\*技术栈偏好\*\*[:：]\s*.+$"),
    re.compile(r"(?m)^\*\*核心领域\*\*[:：]\s*.+$"),
)

OVERVIEW_SYSTEM_PROMPT = """你是资深技术编辑。
你只输出最终答案，不输出思考过程、草稿、解释、提示词复述、示例、标签或代码块。
输出语言必须是简体中文。"""

PROJECT_SYSTEM_PROMPT = """你是资深开源项目分析师。
你只输出最终 Markdown，不输出思考过程、草稿、解释、提示词复述、示例、XML 标签、<think> 标签或代码块围栏。
输出语言必须是简体中文，内容要准确、克制、可读。"""

ENTITY_SYSTEM_PROMPT = """你是资深技术生态分析师。
你只输出最终 Markdown，不输出思考过程、草稿、解释、提示词复述、示例、标签或代码块。
输出语言必须是简体中文。"""

MAX_README_CHARS = 12000

_llm_client = None


def validate_llm_config():
    if not LLM_API_KEY:
        return False, "LLM_API_KEY is not configured"
    if not LLM_BASE_URL:
        return False, "LLM_BASE_URL is not configured"
    return True, None


# 全局 httpx 客户端（绕过 OpenAI SDK 的追踪头问题）
_llm_http_client = None


def get_llm_client():
    """返回兼容 OpenAI SDK 接口的 httpx 客户端"""
    global _llm_http_client

    if _llm_http_client is None:
        is_valid, error = validate_llm_config()
        if not is_valid:
            logger.warning(f"LLM client not initialized: {error}")
            return None
        try:
            import httpx
            # 使用 httpx 直接调用，绕过 OpenAI SDK 的 x-stainless-* 头
            _llm_http_client = httpx.Client(
                timeout=LLM_TIMEOUT,
                base_url=LLM_BASE_URL.rstrip('/') + '/v1',
                headers={
                    "Authorization": f"Bearer {LLM_API_KEY}",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0"
                }
            )
            logger.info(f"LLM client initialized successfully (timeout={LLM_TIMEOUT}s)")
        except Exception as e:
            logger.error(f"Failed to initialize LLM client: {e}")
            return None

    return _llm_http_client


def strip_meta_lines(content):
    if not content:
        return content

    cleaned = content

    think_pattern = r"<think>[\s\S]*?</think>"
    cleaned = re.sub(think_pattern, "", cleaned)

    xml_pattern = r"<[^>]+>"
    cleaned = re.sub(xml_pattern, "", cleaned)

    meta_patterns = [
        r"(?im)^.*?\bpotential output\b.*$",
        r"(?im)^.*?\blet'?s craft final answer\b.*$",
        r"(?im)^.*?\bwait need to ensure\b.*$",
        r"(?im)^.*?\bwe'?ll produce\b.*$",
        r"(?im)^.*?\bcheck that we used\b.*$",
        r"(?im)^.*?\bwrite one sentence\b.*$",
        r"(?im)^.*?\bensure formatting\b.*$",
        r"(?im)^.*?\boutput must\b.*$",
        r"(?im)^.*?\bso just output\b.*$",
        r"(?im)^.*?\bjust the commentary\b.*$",
        r"(?im)^.*?\bhere'?s\b.*$",
        r"(?im)^.*?\banalysis[:：]?\s*$",
        r"(?im)^.*?\bfinal answer[:：]?\s*$",
    ]
    for pattern in meta_patterns:
        cleaned = re.sub(pattern, "", cleaned)

    lines = []
    for line in cleaned.splitlines():
        stripped = line.strip()
        if stripped.startswith("`") and stripped.endswith("`"):
            continue
        lines.append(line.rstrip())

    cleaned = "\n".join(lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def build_overview_prompt(projects):
    project_details = "\n".join(
        [f"- {p['name']}: {p.get('description', 'No description')}" for p in projects]
    )
    return f"""请基于以下 GitHub 热门项目列表，写一段“今日热点”总览。

项目列表：
{project_details}

输出要求：
1. 严格只输出两行。
2. 第一行必须是 Markdown 二级标题，格式：## 今日热点：<主题>
3. 第二行必须是一整段中文，不要分点，不要换行。
4. 第二行需要概括今天的技术主题，并自然点到项目覆盖范围，最后一句固定以“具体项目摘要如下：”结尾。
5. 不要输出任何过程性文字、样例、解释或提示词复述。
"""


def build_project_prompt(project):
    readme_content = (project.get('readme_content') or 'README content not available.')[:MAX_README_CHARS]
    return f"""请基于下面的项目信息，为 GitHub 热榜日报生成一个项目的简明分析。

项目元数据：
- 名称：{project['name']}
- 链接：{project.get('url', '')}
- 描述：{project.get('description', 'N/A')}
- 语言：{project.get('language', 'N/A')}
- Stars：{project.get('stars', 0)}
- Forks：{project.get('forks', 0)}
- Contributor Count：{project.get('contributor_count', 0)}
- Open Issues：{project.get('open_issues', 0)}
- Watchers：{project.get('watchers', 0)}
- Created At：{project.get('created_at', 'N/A')}
- Updated At：{project.get('updated_at', 'N/A')}

README 素材：
{readme_content}

严格输出以下 Markdown 结构，每个要点写实、写具体，不要说空话套话：

### ✨ {project['name']} ({project.get('stars', 0)}★)

> **一句话**：[用一句话说清楚这个项目是干什么的。避免"一个...的工具"这种笼统句式，要让读者读完立刻能想象出它的画面。]

- **它是什么**：[2-3 句话，描述项目的本质和核心功能，让完全不了解的人也能看懂。结合 README 中的实际内容，不要泛泛而谈。]
- **能解决什么痛点**：[1-2 个具体问题，不是"提高效率"这种空话，而是真实场景下开发者会遇到的具体痛点。]
- **适合谁用**：[1-2 类具体的用户群体，比如用某个框架的前端开发者、做数据清洗的 Python 工程师、运维 SRE 等。]
- **怎么上手**：[从 README 中找到最简安装 / 使用方式，给出一行命令或最小代码示例。如果 README 中没有示例，写"文档未提供快速上手示例"。]
- **可以用在哪些场景**：[列出 2-3 个真实落地场景，要具体，比如"搭建内部 API 网关时替代 Nginx 手写配置"而不是"微服务场景"。]
- **技术看点**：[1-2 句，核心技术选型或设计亮點，只写对做技术决策有参考价值的信息。]
- **同类对比**：[如果 README 提到了竞品或有明显对标，点明差异。如果没有明确竞品，写"暂无明显同类对标"即可，不要编造。]
- **注意事项**：[实事求是：上手难度、项目成熟度（结合 issue 数量 / 更新频率 / 创建时间判断）、文档质量、是否有破坏性变更风险等。]

- **GitHub**：[{project['name']}]({project.get('url', '')})

要求：
1. 全部使用简体中文，语气像技术博主分享，读起来自然、有信息量。
2. 每个要点写实，拒绝"赋能""助力""极致体验"等空洞词汇。
3. 未知信息写"暂未提供"，不要编造。
4. 不要输出思考过程、提示词、示例、额外前言或结语。
5. 不要使用代码块围栏包裹整个输出。
"""


def build_entity_prompt(owner, entity_details, top_repos, main_languages):
    top_repos_str = "\n".join(
        [f"- {repo['name']} ({repo['stars']} stars, {repo['language']})" for repo in top_repos]
    ) or "- 暂无代表仓库"
    return f"""请基于以下 GitHub 开发者/组织信息，输出一个极简技术画像。

实体信息：
- 名称：{entity_details.get('name', owner)}
- 类型：{entity_details.get('type', 'N/A')}
- 简介：{entity_details.get('bio', 'N/A')}
- 创建时间：{entity_details.get('created_at', 'N/A')}
- Followers：{entity_details.get('followers', 0)}
- Public Repos：{entity_details.get('public_repos', 0)}

代表仓库：
{top_repos_str}

主要语言：
{main_languages}

只输出下面三行 Markdown，不要多写：
**技术影响力**：一句话概括其在技术社区的位置和影响力
**技术栈偏好**：一句话分析其主要使用的语言和技术方向
**核心领域**：一句话判断其主要聚焦的领域
"""


def call_llm_with_retry(prompt, model, temperature, max_retries=None, delay=None, system_prompt=None):
    import httpx
    import json

    if max_retries is None:
        max_retries = LLM_MAX_RETRIES
    if delay is None:
        delay = LLM_RETRY_DELAY

    client = get_llm_client()
    if client is None:
        logger.error("LLM client not available")
        return None

    last_exception = None
    for attempt in range(max_retries):
        try:
            logger.debug(f"LLM API call attempt {attempt + 1}/{max_retries}")
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            # 直接用 httpx 调用 API
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature
            }
            response = client.post(
                "/chat/completions",
                content=json.dumps(payload),
            )
            if response.status_code != 200:
                raise Exception(f"API returned {response.status_code}: {response.text[:100]}")

            result = response.json()
            raw_content = result.get("choices", [{}])[0].get("message", {}).get("content", "") or ""
            clean_content = strip_meta_lines(raw_content)
            logger.debug(f"LLM API call succeeded on attempt {attempt + 1}")
            return clean_content
        except Exception as e:
            last_exception = e
            error_msg = str(e)
            if "timeout" in error_msg.lower() or "504" in error_msg or "Gateway" in error_msg:
                logger.warning(f"Attempt {attempt + 1}/{max_retries} timed out")
            else:
                logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")

            if attempt < max_retries - 1:
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)

    logger.error(f"All {max_retries} attempts failed. Last error: {last_exception}")
    return None


def extract_overview_intro(content):
    if not content:
        return None

    normalized = strip_meta_lines(content.strip())
    match = OVERVIEW_HEADING_PATTERN.search(normalized)
    if not match:
        return normalized

    remainder = normalized[match.start():].strip()
    lines = remainder.splitlines()
    kept_lines = []
    body_started = False

    for line in lines:
        stripped = line.strip()

        if not kept_lines:
            kept_lines.append(line.rstrip())
            continue

        if not stripped:
            if body_started:
                break
            continue

        if line.startswith("#"):
            break

        kept_lines.append(line.rstrip())
        body_started = True

    cleaned = "\n".join(kept_lines).strip()
    return cleaned or normalized


def extract_project_report(content):
    if not content:
        return None

    normalized = strip_meta_lines(content.strip())
    match = PROJECT_HEADING_PATTERN.search(normalized)
    if not match:
        return normalized

    return normalized[match.start():].strip()


def extract_entity_summary(content):
    if not content:
        return None

    normalized = strip_meta_lines(content.strip())
    lines = []
    for pattern in ENTITY_LINE_PATTERNS:
        match = pattern.search(normalized)
        if match:
            lines.append(match.group(0).strip())

    if lines:
        return "\n".join(lines)

    fallback_lines = []
    for line in normalized.splitlines():
        stripped = line.strip()
        if stripped.startswith("**技术影响力**") or stripped.startswith("**技术栈偏好**") or stripped.startswith("**核心领域**"):
            fallback_lines.append(stripped)

    return "\n".join(fallback_lines).strip() or normalized


def get_entity_summary(owner):
    logger.info(f"Fetching details for entity: {owner}")
    entity_details = get_entity_details(owner)
    if not entity_details:
        return ""

    top_repos = get_entity_repos(owner)
    languages = [repo['language'] for repo in top_repos if repo['language'] and repo['language'] != 'N/A']
    main_languages = ", ".join(
        dict.fromkeys(lang for lang, count in Counter(languages).most_common(3))
    ) if languages else "多样化或未指定"

    prompt = build_entity_prompt(owner, entity_details, top_repos, main_languages)
    summary = call_llm_with_retry(prompt, LLM_MODEL, 0.2, system_prompt=ENTITY_SYSTEM_PROMPT)
    if summary:
        summary = extract_entity_summary(summary)
        return f"\n\n#### 开发者 / 组织速览\n\n{summary}"

    logger.error(f"Error generating entity summary for {owner}")
    return ""


def get_summary_for_single_project(project):
    logger.info(f"Analyzing project: {project['name']}...")
    if 'readme_content' not in project:
        project['readme_content'] = 'README content not available.'

    prompt = build_project_prompt(project)
    project_summary = call_llm_with_retry(prompt, LLM_MODEL, 0.3, system_prompt=PROJECT_SYSTEM_PROMPT)
    if not project_summary:
        logger.error(f"Error calling LLM API for {project['name']}: Failed after retries.")
        return None

    project_summary = extract_project_report(project_summary)

    try:
        owner = project['name'].split('/')[0]
        entity_summary = get_entity_summary(owner)
    except (IndexError, AttributeError):
        entity_summary = ""

    return project_summary + entity_summary


def get_overview_intro(projects):
    logger.info("Generating overview introduction...")
    prompt = build_overview_prompt(projects)

    overview = call_llm_with_retry(prompt, LLM_MODEL, 0.2, system_prompt=OVERVIEW_SYSTEM_PROMPT)
    if overview:
        return extract_overview_intro(overview)

    logger.error("Error calling LLM API for overview: Failed after retries.")
    return "## 今日热点：GitHub 热门趋势\n今天的热门项目覆盖了多个技术方向，具体项目摘要如下："
