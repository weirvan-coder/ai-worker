# -*- coding: utf-8 -*-
import os
import re
from datetime import datetime, timedelta

from config import LOG_DIR


WEEKLY_REVIEW_PROMPT = """你是一位项目复盘教练。请根据用户过去一周的工作日志，生成一份"下周规划"建议。

【本周日志摘要】
{logs_text}

请按以下格式生成下周规划建议（Markdown）：

# 下周规划建议

## 一、本周回顾
- 用 3-5 句话总结本周的主要产出和进展
- 指出本周未能完成或需要跟进的事项

## 二、下周重点目标（3 条）
每条目标格式：
1. 【目标名称】
   - 预期产出：
   - 关键动作（2-3 步）：
   - 优先级：高/中/低

## 三、时间分配建议
| 时段 | 任务类型 | 建议时间占比 |
|------|---------|------------|
| 周一上午 | 规划+确认 | 照常 |
| ...（根据日志内容生成合理建议） |

## 四、风险提醒
- 列出潜在的风险和阻塞项
- 提出预防/应对措施

## 五、自我提升建议
- 基于本周日志的技能/习惯改进建议

要求：
- 建议必须具体、可执行
- 与日志内容紧密结合
- 语气积极、鼓励性
- 使用日期标记（如"下周一（{next_monday}）"）
"""


class LogService:
    """项目日志与复盘服务。

    支持本地 Markdown 日志的读写和时间范围查询。
    可读取指定时间范围内的日志，并生成"下周规划"建议。
    """

    LOG_DIR = LOG_DIR

    @classmethod
    def write_log(cls, content: str, date_str: str = "") -> str:
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_str}.md"
        filepath = os.path.join(cls.LOG_DIR, filename)

        mode = "a" if os.path.exists(filepath) else "w"
        with open(filepath, mode, encoding="utf-8") as f:
            if mode == "w":
                f.write(f"# 工作日志 - {date_str}\n\n")
            timestamp = datetime.now().strftime("%H:%M")
            f.write(f"### {timestamp}\n\n{content}\n\n")

        return filepath

    @classmethod
    def read_logs(cls, days: int = 7) -> list[dict]:
        today = datetime.now().date()
        logs = []
        for i in range(days):
            date = today - timedelta(days=i)
            filename = f"{date.strftime('%Y-%m-%d')}.md"
            filepath = os.path.join(cls.LOG_DIR, filename)
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    logs.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "weekday": ["周一","周二","周三","周四","周五","周六","周日"][date.weekday()],
                        "filepath": filepath,
                        "content": f.read(),
                    })
        logs.sort(key=lambda x: x["date"])
        return logs

    @classmethod
    def build_weekly_prompt(cls, logs: list[dict]) -> str:
        if not logs:
            return ""

        log_parts = []
        for log in logs:
            log_parts.append(
                f"\n### {log['date']} ({log['weekday']})\n{log['content'][:1500]}"
            )
        logs_text = "\n".join(log_parts)

        next_monday = datetime.now().date()
        while next_monday.weekday() != 0:
            next_monday += timedelta(days=1)

        return WEEKLY_REVIEW_PROMPT.format(
            logs_text=logs_text,
            next_monday=next_monday.strftime("%m-%d"),
        )

    @classmethod
    def save_weekly_plan(cls, content: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        monday = datetime.now().date()
        while monday.weekday() != 0:
            monday -= timedelta(days=1)
        week_tag = monday.strftime("%Y%m%d")
        filename = f"plan_{week_tag}_{timestamp}.md"
        filepath = os.path.join(cls.LOG_DIR, filename)

        full_content = (
            f"{content}\n\n---\n> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_content)
        return filepath

    @classmethod
    def list_plans(cls) -> list[str]:
        files = sorted(
            [f for f in os.listdir(cls.LOG_DIR) if f.startswith("plan_") and f.endswith(".md")],
            reverse=True,
        )
        return [os.path.join(cls.LOG_DIR, f) for f in files]
