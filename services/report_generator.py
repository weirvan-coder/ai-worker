# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

from config import REPORT_DIR


STRUCTURED_REPORT_PROMPT = """你是一位资深行业分析师。请根据以下网络搜集的资料，生成一份结构化的调研报告。

【源资料】
{source_material}

请严格按照以下结构生成报告（Markdown 格式），每个章节都要有实质性内容：

# {title}

## 一、背景
- 阐述本调研主题的宏观背景、行业现状和调研目的
- 说明为什么这个主题在当前具有重要性
- 如有必要，列出研究方法论

## 二、核心结论
以编号列表形式列出 3-5 条最重要的结论，每条结论：
- 用一句话概括核心观点
- 用 【】 标注置信度（高/中/低）
- 句末标注信息来源编号，如 [来源1]

## 三、数据支撑
针对每条核心结论，提供：
- 具体的定量数据（百分比、增长率、金额等）
- 定性分析（专家观点、趋势判断等）
- 数据来源与时效说明

## 四、风险评估
- 识别当前主题涉及的主要风险
- 对每条风险说明影响程度和发生概率
- 提出缓解措施建议

## 五、总结与建议
- 200 字以内的整体总结
- 3 条可操作的具体建议
- 未来 6-12 个月的趋势展望

## 六、信息来源
列出所有引用来源的编号、标题和 URL

要求：
- 语言专业、客观、数据驱动
- 避免空泛描述，所有结论必须有资料支撑
- 报告中提及数据时，务必注明来源
"""


class ReportGenerator:
    """结构化报告生成服务。

    接收已抓取的网页内容作为原始素材，
    使用指定的提示词模板生成包含"背景-核心结论-数据支撑"的深度报告。
    """

    @staticmethod
    def build_report_prompt(title: str, materials: list[dict]) -> str:
        source_parts = []
        for i, m in enumerate(materials, 1):
            source_parts.append(
                f"\n{'='*60}\n"
                f"[来源{i}] {m.get('title', '无标题')}\n"
                f"URL: {m.get('url', '')}\n"
                f"{'='*60}\n"
                f"{m.get('content', '')[:4000]}"
            )
        source_text = "\n".join(source_parts)

        return STRUCTURED_REPORT_PROMPT.format(
            title=title,
            source_material=source_text,
        )

    @classmethod
    def save_report(cls, title: str, content: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(
            c if c.isalnum() or c in "._- " else "_" for c in title
        )
        safe_title = safe_title.strip().replace(" ", "_")[:60]
        filename = f"report_{timestamp}_{safe_title}.md"
        filepath = os.path.join(REPORT_DIR, filename)

        full_content = (
            f"# {title}\n\n"
            f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"> 类型: 结构化调研报告\n\n"
            f"{content}"
        )
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_content)
        return filepath

    @classmethod
    def list_reports(cls) -> list[str]:
        files = sorted(
            [f for f in os.listdir(REPORT_DIR) if f.startswith("report_") and f.endswith(".md")],
            reverse=True,
        )
        return [os.path.join(REPORT_DIR, f) for f in files]
