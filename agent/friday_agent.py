# -*- coding: utf-8 -*-
from agentscope.agent import ReActAgent
from agentscope.model import (
    DashScopeChatModel,
    OpenAIChatModel,
    GeminiChatModel,
    OllamaChatModel,
)
from agentscope.formatter import (
    DashScopeChatFormatter,
    OpenAIChatFormatter,
    GeminiChatFormatter,
    OllamaChatFormatter,
    DeepSeekChatFormatter,
)
from agentscope.memory import InMemoryMemory

from config import get_model_config
from agent.tools import build_toolkit

SYSTEM_PROMPT = """你是一位专业的研究分析助手，名叫 Friday。你拥有三大核心技能：调研报告生成、PPT 演示制作、项目复盘规划。

## 技能总览

| 技能 | 触发方式 | 核心工具 |
|------|---------|---------|
| 🔍 调研报告 | 用户提出研究问题 | search_web → fetch_webpage → generate_structured_report → save_report |
| 📊 PPT 生成 | 用户说"生成PPT/幻灯片" | 基于已有报告大纲 → save_pptx_report |
| 📋 项目复盘 | 用户说"复盘/周报/下周规划" | write_log → read_weekly_logs → generate_weekly_plan → save_report |

---

## 技能一：调研报告生成

### 工作流程
1. 理解需求，确定研究主题和范围
2. 使用 `search_web` 多轮搜索（至少 2-3 轮，不同关键词角度）
3. 对最重要的搜索结果，使用 `fetch_webpage` 抓取详细内容
4. 收集到 1-3 个来源 URL 后，调用 `generate_structured_report(title, url1, url2, url3)`
   - 此工具会自动抓取内容并生成包含提示词的报告指令
   - 接着按照返回的提示词格式，生成一份完整的 Markdown 报告
5. 使用 `save_report` 保存最终报告

### 报告结构（必须严格遵循）
- **背景**：宏观背景、行业现状、研究目的
- **核心结论**：3-5 条结论，标注置信度【高/中/低】，注明来源编号 [来源1]
- **数据支撑**：定量数据 + 定性分析，每项标注来源
- **风险评估**：识别风险 + 影响程度 + 缓解措施
- **总结与建议**：200 字总结 + 3 条可执行建议 + 6-12 月展望
- **信息来源**：所有引用来源的编号、标题、URL

---

## 技能二：PPT 生成

### 触发方式
用户明确说"生成 PPT""转成幻灯片""导出 PPTX"等。

### 工作流程
1. **先确保已有报告大纲**：如果当前对话中还没有报告，请先使用技能一生成报告
2. 提取报告中的大纲（用 ## 标题组织各章节）
3. 调用 `save_pptx_report(title, outline)` 
   - title 用报告标题
   - outline 用报告大纲（每行一个 ## 章节名，后跟内容要点）
4. PPT 会自动生成：深色封面页 → 各章节内容页（白底 + 蓝色分隔线）

### 大纲格式示例
```
## 背景
（背景章节要点...）
## 核心结论
（结论章节要点...）
## 数据支撑
（数据章节要点...）
```

---

## 技能三：项目复盘与周规划

### 触发方式
用户说"复盘""这周总结""下周规划""周报""写日志"等。

### 记录日志
用户说"写日志/记录一下"时，调用 `write_log(content)` 追加到当天日志。

### 生成本周复盘 + 下周规划
1. 调用 `read_weekly_logs(days=7)` 读取最近一周日志
2. 调用 `generate_weekly_plan()` 生成复盘指令
3. 按照返回的提示词格式，生成包含以下内容的规划：
   - **本周回顾**：3-5 句总结 + 未完成跟进
   - **下周重点目标**：3 条目标，每条有预期产出、关键动作、优先级
   - **时间分配建议**：表格形式
   - **风险提醒**：潜在风险 + 应对措施
   - **自我提升建议**：技能/习惯改进
4. 使用 `save_report` 保存规划

---

## 通用工具
- `list_reports`：列出所有已生成的研究报告和下周规划文件
- `write_log`：随时记录工作日志
- `fetch_webpage`：获取任意网页内容

## 注意事项
- 调研报告务必多轮搜索、多来源交叉验证
- 报告语言与用户提问语言保持一致
- 所有报告完成后必须用对应工具保存
- PPT 必须基于已生成的报告内容，不要凭空编造
- 复盘规划必须基于实际日志内容，没有日志时提示用户先记录
"""


def create_model():
    cfg = get_model_config()
    provider = cfg["provider"]

    _builders = {
        "ollama": _build_ollama,
        "dashscope": _build_dashscope,
        "openai": _build_openai,
        "gemini": _build_gemini,
        "deepseek": _build_deepseek,
        "custom": _build_custom,
    }

    builder = _builders.get(provider)
    if not builder:
        raise ValueError(f"未知的 provider: {provider}")
    return builder(cfg)


def _build_ollama(cfg):
    model_name = cfg["model_name"]
    host = cfg.get("host", "http://localhost:11434")
    print(f"[INFO] 使用 Ollama 本地模型: {model_name} @ {host}")
    return (
        OllamaChatModel(
            model_name=model_name,
            host=host,
            stream=True,
        ),
        OllamaChatFormatter(),
    )


def _build_dashscope(cfg):
    model_name = cfg["model_name"]
    api_key = cfg["api_key"]
    print(f"[INFO] 使用 DashScope 模型: {model_name}")
    return (
        DashScopeChatModel(
            model_name=model_name,
            api_key=api_key,
            stream=True,
        ),
        DashScopeChatFormatter(),
    )


def _build_openai(cfg):
    model_name = cfg["model_name"]
    api_key = cfg["api_key"]
    base_url = cfg.get("base_url")
    display = f"{model_name}" + (f" @ {base_url}" if base_url else "")
    print(f"[INFO] 使用 OpenAI 模型: {display}")

    client_kwargs = {}
    if base_url:
        client_kwargs["base_url"] = base_url

    return (
        OpenAIChatModel(
            model_name=model_name,
            api_key=api_key,
            stream=True,
            client_kwargs=client_kwargs or None,
        ),
        OpenAIChatFormatter(),
    )


def _build_gemini(cfg):
    model_name = cfg["model_name"]
    api_key = cfg["api_key"]
    print(f"[INFO] 使用 Gemini 模型: {model_name}")
    return (
        GeminiChatModel(
            model_name=model_name,
            api_key=api_key,
            stream=True,
        ),
        GeminiChatFormatter(),
    )


def _build_deepseek(cfg):
    model_name = cfg["model_name"]
    api_key = cfg["api_key"]
    base_url = cfg.get("base_url", "https://api.deepseek.com/v1")
    print(f"[INFO] 使用 DeepSeek 模型: {model_name} @ {base_url}")
    return (
        OpenAIChatModel(
            model_name=model_name,
            api_key=api_key,
            stream=True,
            client_kwargs={"base_url": base_url},
        ),
        DeepSeekChatFormatter(),
    )


def _build_custom(cfg):
    model_name = cfg["model_name"]
    api_key = cfg["api_key"]
    base_url = cfg["base_url"]
    provider_info = cfg.get("provider_info", model_name)
    print(f"[INFO] 使用自定义 OpenAI 兼容模型: {provider_info} @ {base_url}")
    return (
        OpenAIChatModel(
            model_name=model_name,
            api_key=api_key,
            stream=True,
            client_kwargs={"base_url": base_url},
        ),
        OpenAIChatFormatter(),
    )


def create_agent():
    model, formatter = create_model()
    toolkit = build_toolkit()

    agent = ReActAgent(
        name="Friday",
        sys_prompt=SYSTEM_PROMPT,
        model=model,
        formatter=formatter,
        memory=InMemoryMemory(),
        toolkit=toolkit,
    )
    return agent
