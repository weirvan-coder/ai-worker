# -*- coding: utf-8 -*-
import os
from datetime import datetime

from config import REPORT_DIR


class ReportService:
    """报告生成服务。

    负责将研究内容格式化并输出为文件。
    当前支持 Markdown 格式，后续可扩展 PPT / PDF / HTML 等格式。
    """

    OUTPUT_DIR = REPORT_DIR

    @classmethod
    def save_markdown(cls, title: str, content: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(
            c if c.isalnum() or c in "._- " else "_" for c in title
        )
        safe_title = safe_title.strip().replace(" ", "_")[:60]
        filename = f"{timestamp}_{safe_title}.md"
        filepath = os.path.join(cls.OUTPUT_DIR, filename)

        full_content = (
            f"# {title}\n\n"
            f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"{content}"
        )
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_content)

        return filepath

    @classmethod
    def list_reports(cls) -> list[str]:
        files = sorted(
            [f for f in os.listdir(cls.OUTPUT_DIR) if f.endswith(".md")],
            reverse=True,
        )
        return [os.path.join(cls.OUTPUT_DIR, f) for f in files]
