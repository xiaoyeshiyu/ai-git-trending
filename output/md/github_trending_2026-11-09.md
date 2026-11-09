## 今日热点：GitHub 热门趋势
今天的热门项目覆盖了多个技术方向，具体项目摘要如下：

### ✨ anthropics/skills (178096★)

> **一句话**：这是 Anthropic 为 Claude 提供的一组可直接参考和安装的 Agent Skills 示例，把文档处理、设计开发、API 使用等复杂任务整理成 Claude 能动态加载的指令、脚本与资源。

- **它是什么**：项目以独立文件夹组织每个 Skill，每个 Skill 通过 `SKILL.md` 描述元数据、使用条件和执行指令，Claude 可在需要时加载它们来完成特定任务。仓库覆盖创意与设计、开发技术、企业沟通以及 DOCX、PDF、PPTX、XLSX 文档处理，并同时提供 Agent Skills 规范和模板。

- **能解决什么痛点**：开发者不必每次都从头编写复杂的提示词、操作步骤和领域约束，可以把一套重复工作的流程固化为可复用 Skill。对于文档生成、表格处理、前端设计或 Claude API 集成等任务，它还提供了接近真实生产场景的参考实现，降低自行摸索格式和调用方式的成本。

- **适合谁用**：使用 Claude Code、Claude.ai 或 Claude API 构建智能代理的开发者；希望把企业品牌规范、文档处理流程、测试流程或内部工作流封装成可复用能力的团队。

- **怎么上手**：在 Claude Code 中执行 `/plugin marketplace add anthropics/skills`，随后安装 `document-skills` 或 `example-skills` 插件；也可以直接执行 `/plugin install document-skills@anthropic-agent-skills`。创建自定义 Skill 时，可按 README 提供的模板建立目录，并在 `SKILL.md` 中填写 `name` 和 `description`。

- **可以用在哪些场景**：
  - 让 Claude 按公司品牌规范生成演示文稿、报告、表格和 PDF 文档。
  - 将 Claude API 的 SDK 升级、模型更新、Managed Agents 配置等开发流程整理为可查询和执行的 Skill。
  - 为内部数据分析、网页测试、MCP Server 生成或企业沟通流程提供固定的操作指令和示例资源。

- **技术看点**：Skill 采用“目录 + `SKILL.md` + 可选脚本和资源”的轻量结构，通过 YAML frontmatter 声明名称与适用描述，便于 Claude 按任务动态加载。仓库同时维护示例实现、Skill 规范和模板，既能直接安装，也能作为构建自定义 Agent 能力的参考基线。

- **近期动向与发展方向**：近期提交明显集中在 `claude-api` Skill，持续跟进 SDK 1.x 升级、模型版本、Managed Agents、权限策略、成本优化和 API 文档变化，说明项目重点是同步 Anthropic 平台的快速演进。与此同时，项目还更新了 `frontend-design`、文档类 Skills，并新增 `academy-guide` 和 `discernment-nudge`；近 20 条提交覆盖 2026 年 5 月至 9 月，维护节奏较活跃，但提交主要由少数核心贡献者推动，16 名贡献者的规模仍偏小。

- **同类对比**：暂无明显同类对标。README 明确区分了本仓库的 Anthropic 实现与 [Agent Skills 标准](http://agentskills.io)，前者更偏向 Claude 的示例、插件和生产参考实现，后者是可供其他实现遵循的规范。

- **注意事项**：项目创建于 2025 年 9 月，已经积累 17.8 万 Stars，但同时有 1293 个开放 Issue，需求和反馈规模较大。部分 Skill，尤其是文档创建与编辑相关实现，是 source-available 而非 Apache 2.0 开源；仓库也声明内容主要用于演示和教育，实际行为可能随 Claude 或 API 版本变化。近期频繁跟进模型、SDK 和平台功能，上手时应核对对应文档与版本，避免因 API 或 Skill 内容更新产生兼容性问题。

- **GitHub**：[anthropics/skills](https://github.com/anthropics/skills)

#### 开发者 / 组织速览

**技术影响力**：拥有近 8.8 万关注者，多个仓库获数万至十余万星，是 AI 开发者生态中的高影响力组织。
**技术栈偏好**：以 Python、Jupyter Notebook 和 TypeScript 为主，覆盖 AI 工具开发、交互式教程与应用示例。
**核心领域**：聚焦 Claude 相关开发工具、技能与提示工程，并拓展至金融等行业应用。

---

### ✨ meta/astryx (19368★)

> **一句话**：该项目已进入今日 GitHub Trending，但本次暂未成功生成 AI 分析。

- **它是什么**：An open source design system that's fully customizable and agent ready
- **能解决什么痛点**：暂未提供。
- **适合谁用**：暂未提供。
- **怎么上手**：文档未提供快速上手示例。
- **可以用在哪些场景**：暂未提供。
- **技术看点**：暂未提供。
- **近期动向与发展方向**：暂无 commit 数据可用。
- **同类对比**：暂无明显同类对标。
- **注意事项**：AI 分析暂未生成，建议直接查看项目 README 和 Issue 状态。

- **GitHub**：[meta/astryx](https://github.com/meta/astryx)


---

### ✨ sherlock-project/sherlock (106637★)

> **一句话**：该项目已进入今日 GitHub Trending，但本次暂未成功生成 AI 分析。

- **它是什么**：Hunt down social media accounts by username across social networks
- **能解决什么痛点**：暂未提供。
- **适合谁用**：暂未提供。
- **怎么上手**：文档未提供快速上手示例。
- **可以用在哪些场景**：暂未提供。
- **技术看点**：暂未提供。
- **近期动向与发展方向**：暂无 commit 数据可用。
- **同类对比**：暂无明显同类对标。
- **注意事项**：AI 分析暂未生成，建议直接查看项目 README 和 Issue 状态。

- **GitHub**：[sherlock-project/sherlock](https://github.com/sherlock-project/sherlock)


---

### ✨ google-deepmind/mujoco (16824★)

> **一句话**：该项目已进入今日 GitHub Trending，但本次暂未成功生成 AI 分析。

- **它是什么**：Multi-Joint dynamics with Contact. A general purpose physics simulator.
- **能解决什么痛点**：暂未提供。
- **适合谁用**：暂未提供。
- **怎么上手**：文档未提供快速上手示例。
- **可以用在哪些场景**：暂未提供。
- **技术看点**：暂未提供。
- **近期动向与发展方向**：暂无 commit 数据可用。
- **同类对比**：暂无明显同类对标。
- **注意事项**：AI 分析暂未生成，建议直接查看项目 README 和 Issue 状态。

- **GitHub**：[google-deepmind/mujoco](https://github.com/google-deepmind/mujoco)


---

### ✨ anthropics/claude-quickstarts (19895★)

> **一句话**：该项目已进入今日 GitHub Trending，但本次暂未成功生成 AI 分析。

- **它是什么**：A collection of projects designed to help developers quickly get started with building deployable applications using the Claude API
- **能解决什么痛点**：暂未提供。
- **适合谁用**：暂未提供。
- **怎么上手**：文档未提供快速上手示例。
- **可以用在哪些场景**：暂未提供。
- **技术看点**：暂未提供。
- **近期动向与发展方向**：暂无 commit 数据可用。
- **同类对比**：暂无明显同类对标。
- **注意事项**：AI 分析暂未生成，建议直接查看项目 README 和 Issue 状态。

- **GitHub**：[anthropics/claude-quickstarts](https://github.com/anthropics/claude-quickstarts)


---

### ✨ garrytan/gbrain (32024★)

> **一句话**：该项目已进入今日 GitHub Trending，但本次暂未成功生成 AI 分析。

- **它是什么**：Garry's Opinionated OpenClaw/Hermes Agent Brain
- **能解决什么痛点**：暂未提供。
- **适合谁用**：暂未提供。
- **怎么上手**：文档未提供快速上手示例。
- **可以用在哪些场景**：暂未提供。
- **技术看点**：暂未提供。
- **近期动向与发展方向**：暂无 commit 数据可用。
- **同类对比**：暂无明显同类对标。
- **注意事项**：AI 分析暂未生成，建议直接查看项目 README 和 Issue 状态。

- **GitHub**：[garrytan/gbrain](https://github.com/garrytan/gbrain)


---

### ✨ vercel-labs/agent-browser (48320★)

> **一句话**：该项目已进入今日 GitHub Trending，但本次暂未成功生成 AI 分析。

- **它是什么**：Browser automation CLI for AI agents
- **能解决什么痛点**：暂未提供。
- **适合谁用**：暂未提供。
- **怎么上手**：文档未提供快速上手示例。
- **可以用在哪些场景**：暂未提供。
- **技术看点**：暂未提供。
- **近期动向与发展方向**：暂无 commit 数据可用。
- **同类对比**：暂无明显同类对标。
- **注意事项**：AI 分析暂未生成，建议直接查看项目 README 和 Issue 状态。

- **GitHub**：[vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)


---

### ✨ ruvnet/RuView (93692★)

> **一句话**：RuView 让 ESP32 读取 WiFi 信号反射变化，在不使用摄像头或穿戴设备的情况下，实时判断房间里是否有人、如何移动以及呼吸和心率趋势。

- **它是什么**：这是一个基于 Rust 的 WiFi CSI 感知平台，将低成本 ESP32 节点采集到的信道状态信息转换为存在检测、人数统计、活动识别、跌倒检测、呼吸和心率监测等结果。它支持边缘侧运行、局部环境校准，并可通过 MQTT、Matter、Apple Home、Google Home 和 Alexa 接入智能家居。

- **能解决什么痛点**：在卧室、养老房间或卫生间等不适合安装摄像头的区域，仍需要持续判断有人活动、离床、跌倒或长时间不动。对不愿佩戴手环、胸带等设备的人，RuView提供了非接触式的呼吸、心率和睡眠监测方案。

- **适合谁用**：适合使用 ESP32、Raspberry Pi 和 Home Assistant 搭建隐私敏感型智能家居或边缘感知系统的开发者。也适合研究 WiFi CSI、无线感知、无摄像头姿态估计和时序信号模型的工程团队。

- **怎么上手**：README 提供的 MetaHarness 最小入口是 `npx @ruvnet/ruview@0.4.0 doctor`；接入 Home Assistant 可直接运行带 `--mqtt` 参数的 RuView 服务，具体启动命令需结合部署方式查看项目文档。

- **可以用在哪些场景**：
  - 在 Home Assistant 中发布房间有人、睡眠、离床、跌倒风险和活动状态，联动灯光、空调或告警。
  - 在养老院或家庭卧室中进行夜间呼吸、心率趋势和异常静止监测，减少摄像头带来的隐私问题。
  - 在办公室、商店或工业区域部署多个 ESP32 节点，统计占用人数、进出流动和跨房间移动，不要求人员携带标签。

- **技术看点**：项目采用 Rust 构建从 CSI 采集、信号处理、推理到边缘服务的完整链路，支持 ESP32 Mesh、多频段信道跳转、TDM 调度和本地模型推理。其设计还引入了不确定性、来源、隐私策略和 Ed25519 witness chain 等治理信息，但 README 同时注明统一 RF 世界模型在真实数据验证前仍属于合成精度阶段。

- **近期动向与发展方向**：最近提交高度集中在固件和边缘节点可靠性建设，包括 ESP32-C6 的 USB onboarding、macOS RSSI 感知、节点持久化日志、Flash coredump、16MB Flash 配置和天线选择。服务端与推理链路也在持续修复 RSSI 哨兵污染、节点位置融合、训练损失导出和 CSI 指标问题，说明项目当前重点是扩展硬件部署能力、提高采集稳定性并校正模型训练与评测结果；近期开提交密集，且有 `rUv`、`clonea1`、`Faizan` 等贡献者参与，但整体贡献者数量为 39 人。

- **同类对比**：README 未明确列出直接竞品；项目明显区别于摄像头姿态估计、毫米波雷达和可穿戴设备方案，核心卖点是利用普通 WiFi 与低成本 ESP32 进行非视觉、非接触式感知，同时也预留 WiFi CSI、雷达、UWB 和蜂窝感知的统一融合模型。

- **注意事项**：项目创建于 2025 年 6 月，却已达到 93692 Stars、12421 Forks 和 708 个 Open Issues，功能范围很大，实际成熟度不能只按热度判断。README 对部分能力有明确限制：已提交的 `pose_v1` 模型 PCK@20 仅为 3.0%，运行路径仍是 `confidence=0` 的桩实现；82.3% 和 82.69% 等指标对应特定数据集或独立模型，不能直接等同于真实家庭环境效果。部署还涉及 ESP32 硬件、CSI 采集、环境校准和模型选择，文档内容较多，上手成本高于普通 Home Assistant 插件；医疗监测、跌倒告警等场景应进行现场验证，不能将输出直接当作诊断结论。

- **GitHub**：[ruvnet/RuView](https://github.com/ruvnet/RuView)

#### 开发者 / 组织速览

**技术影响力**：高影响力开源开发者，凭借多个高星项目在 GitHub 技术社区具备较强关注度。
**技术栈偏好**：偏好 TypeScript 与 Rust，重视高性能系统、开发工具及现代应用架构。
**核心领域**：主要聚焦 AI Agent、智能工作流、向量计算与相关基础设施。

---

### ✨ ZhuLinsen/daily_stock_analysis (61034★)

> **一句话**：它把自选股票、行情、新闻、技术指标和大模型分析串成一条自动化流水线，每天生成一份可直接推送到企业微信、飞书、Telegram、Discord、Slack 或邮箱的“决策仪表盘”。

- **它是什么**：这是一个用 Python 写的多市场股票智能分析系统，覆盖 A 股、港股、美股、日股、韩股、台股和 ETF。它会聚合多源行情、实时新闻、公告和基本面信息，再交给 LLM 生成分析结论、评分、风险提示和买卖点位，并能通过 Web 工作台、定时任务和自动通知跑起来。
- **能解决什么痛点**：一是把原本分散在行情站、新闻搜索、研报和聊天记录里的信息整理成一份固定格式的日报，避免人工每天来回切换页面。二是把“看盘、搜新闻、写总结、发群里”这类重复工作自动化，尤其适合需要长期盯多个市场和多只标的的场景。
- **适合谁用**：做量化研究、投研辅助、私募/散户自建盯盘系统的人；以及需要在 Python 生态里接入行情源、新闻源和 LLM 的开发者。对想用 GitHub Actions、Docker 或本地定时任务做自动报告推送的人也比较合适。
- **怎么上手**：README 给出的最小本地运行方式是先安装依赖再启动主程序：`git clone https://github.com/ZhuLinsen/daily_stock_analysis.git && cd daily_stock_analysis && pip install -r requirements.txt && python main.py`。
- **可以用在哪些场景**：每天固定生成自选股晨报或收盘复盘，发到企业微信/飞书群里；把 A/H/美股的新闻、公告和行情合并后做跨市场对比分析；在 Web 工作台里人工发起一次分析，查看完整 Markdown 报告和历史记录。
- **技术看点**：项目的核心不是单一策略，而是“数据源优先级 + LLM 分析 + 多渠道推送”的组合设计，支持免费行情源与 token 型数据源并存，也支持 OpenAI 兼容、DeepSeek、通义千问、Claude、Ollama 等多种模型后端。README 里还明确了 GitHub Actions、Docker、本地定时任务和 FastAPI/Web UI 这几条运行路径，部署弹性比较大。
- **近期动向与发展方向**：最近 20 条提交里，主线非常清楚，集中在 v3.29.0 到 v3.30.0 的发布准备、分享图功能修复、移动端交互修复、前后端稳定性增强和 CI 加速。除了持续修 bug，还在补 `Responses API` 路由、会话级技能选择、Lark 国际域名、后台测试分片等能力，说明项目正沿着“更稳定的多端体验 + 更强的模型/通知编排 + 更成熟的测试与发布流程”推进，且贡献者不止一位，社区活跃度较高。
- **同类对比**：README 里明确提到它聚焦“日常分析报告”，并与 `AlphaSift`、`AlphaEvo` 区分开来：前者更偏选股实现参考，后者偏策略回测与自我进化，而这个项目更像是面向日常使用的分析与推送工作台。
- **注意事项**：项目功能面很宽，上手前要先准备 LLM Key、通知渠道和至少一条自选股配置，否则只能跑到一半。它的 Stars 和 Forks 很高，说明关注度和传播度都不错，但 Open Issues 也有 40 个，配合近期持续修复和重构迹象来看，仍处在高活跃维护期，接口、数据源和推送链路都可能随着版本迭代出现行为变化；免费数据源虽然可零成本运行，但 README 也明确说了稳定性不保证。

- **GitHub**：[ZhuLinsen/daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis)

#### 开发者 / 组织速览

**技术影响力**：具备较高社区影响力，拥有一个高关注度开源项目及一定开发者关注基础。
**技术栈偏好**：以 Python 为主，偏好数据分析、智能代理与自动化工具开发。
**核心领域**：主要聚焦 LLM、AIGC、量化分析与机器人智能化。

---

### ✨ homeassistant-ai/ha-mcp (5763★)

> **一句话**：该项目已进入今日 GitHub Trending，但本次暂未成功生成 AI 分析。

- **它是什么**：Configure and automate Home Assistant with Claude, ChatGPT, and other AI assistants.
- **能解决什么痛点**：暂未提供。
- **适合谁用**：暂未提供。
- **怎么上手**：文档未提供快速上手示例。
- **可以用在哪些场景**：暂未提供。
- **技术看点**：暂未提供。
- **近期动向与发展方向**：暂无 commit 数据可用。
- **同类对比**：暂无明显同类对标。
- **注意事项**：AI 分析暂未生成，建议直接查看项目 README 和 Issue 状态。

- **GitHub**：[homeassistant-ai/ha-mcp](https://github.com/homeassistant-ai/ha-mcp)


---

### ✨ milind-soni/OpenMausBot (19494★)

> **一句话**：该项目已进入今日 GitHub Trending，但本次暂未成功生成 AI 分析。

- **它是什么**：Open-source Grok Bot alternative with a virtual machine that bots can use
- **能解决什么痛点**：暂未提供。
- **适合谁用**：暂未提供。
- **怎么上手**：文档未提供快速上手示例。
- **可以用在哪些场景**：暂未提供。
- **技术看点**：暂未提供。
- **近期动向与发展方向**：暂无 commit 数据可用。
- **同类对比**：暂无明显同类对标。
- **注意事项**：AI 分析暂未生成，建议直接查看项目 README 和 Issue 状态。

- **GitHub**：[milind-soni/OpenMausBot](https://github.com/milind-soni/OpenMausBot)
