# -*- coding: utf-8 -*-
import os

from agentscope.tool import Toolkit, ToolResponse

from services import (
    SearchService,
    ReportService,
    ReportGenerator,
    PPTService,
    LogService,
)

_search_service = SearchService()


def build_toolkit() -> Toolkit:
    toolkit = Toolkit()

    @toolkit.register_tool_function
    def search_web(query: str, max_results: int = 5) -> ToolResponse:
        """搜索互联网获取信息。使用不同的关键词多轮搜索可获得更全面的结果。"""
        try:
            results = _search_service.search(query, max_results)
            formatted = SearchService.format_results(results)
            return ToolResponse(content=formatted)
        except Exception as e:
            return ToolResponse(content=f"搜索出错: {str(e)}")

    @toolkit.register_tool_function
    def fetch_webpage(url: str, max_chars: int = 8000) -> ToolResponse:
        """获取指定网页的文本内容。用于深入阅读搜索结果中的页面。"""
        try:
            content = _search_service.fetch_page(url, max_chars)
            if not content.strip():
                return ToolResponse(content="未能提取到网页文本内容。")
            return ToolResponse(content=content)
        except Exception as e:
            return ToolResponse(content=f"获取网页出错: {str(e)}")

    @toolkit.register_tool_function
    def save_report(title: str, content: str) -> ToolResponse:
        """将 Markdown 格式的最终报告保存到本地文件。"""
        try:
            filepath = ReportService.save_markdown(title, content)
            filename = os.path.basename(filepath)
            return ToolResponse(
                content=f"报告已保存成功！\n文件位置: {filepath}\n文件名: {filename}"
            )
        except Exception as e:
            return ToolResponse(content=f"保存报告出错: {str(e)}")

    @toolkit.register_tool_function
    def generate_structured_report(
        title: str,
        source_url1: str = "",
        source_url2: str = "",
        source_url3: str = "",
    ) -> ToolResponse:
        """抓取指定网页后，生成包含"背景-核心结论-数据支撑"的结构化深度调研报告。
        你需要先使用 search_web 找到 URL，然后传入 1-3 个来源 URL。
        此工具会自动抓取网页内容并生成格式化报告，你只需把返回的 content 用 save_report 保存即可。
        
        Args:
            title: 报告标题
            source_url1: 第一个来源网页 URL（必填）
            source_url2: 第二个来源网页 URL（可选）
            source_url3: 第三个来源网页 URL（可选）
        """
        try:
            urls = [u for u in [source_url1, source_url2, source_url3] if u.strip()]
            if not urls:
                return ToolResponse(content="请至少提供一个来源 URL")

            materials = []
            for i, url in enumerate(urls):
                page_content = _search_service.fetch_page(url, max_chars=5000)
                materials.append({
                    "title": f"来源网页 {i+1}",
                    "url": url,
                    "content": page_content,
                })

            prompt = ReportGenerator.build_report_prompt(title, materials)
            return ToolResponse(
                content=(
                    f"--- 报告生成指令 ---\n"
                    f"请根据以下资料，严格按照提示词结构生成报告。\n"
                    f"报告标题: {title}\n\n"
                    f"{prompt}\n\n"
                    f"--- 请生成完整的 Markdown 格式报告，并用 save_report 保存 ---"
                )
            )
        except Exception as e:
            return ToolResponse(content=f"生成报告出错: {str(e)}")

    @toolkit.register_tool_function
    def save_pptx_report(
        title: str,
        outline: str,
    ) -> ToolResponse:
        """将调研报告大纲转换为 PPTX 演示文稿并保存。
        当用户说"生成PPT"或"转成幻灯片"时使用此工具。
        
        Args:
            title: PPT 标题（会显示在封面页）
            outline: 报告大纲（Markdown 格式，以 ## 章节标题组织）
        """
        try:
            slides_data = PPTService.build_outline_slides(outline)
            if not slides_data:
                return ToolResponse(content="报告大纲为空，无法生成 PPT")

            title_slide = {"type": "title", "title": title, "content": "AI Worker · Friday 自动生成"}
            slides_data.insert(0, title_slide)

            filepath = PPTService.create_pptx(
                title=title,
                slides_data=slides_data,
                template_path=os.getenv("PPT_TEMPLATE_PATH", ""),
            )
            filename = os.path.basename(filepath)
            return ToolResponse(
                content=f"PPT 已生成成功！\n文件位置: {filepath}\n文件名: {filename}\n共 {len(slides_data)} 页"
            )
        except Exception as e:
            return ToolResponse(content=f"生成 PPT 出错: {str(e)}")

    @toolkit.register_tool_function
    def read_weekly_logs(days: int = 7) -> ToolResponse:
        """读取指定天数内的本地日志文件。用于项目复盘和回顾。
        
        Args:
            days: 读取最近多少天的日志，默认 7 天
        """
        try:
            logs = LogService.read_logs(days)
            if not logs:
                return ToolResponse(
                    content=f"最近 {days} 天内没有找到日志文件。\n"
                            f"日志目录: {LogService.LOG_DIR}\n"
                            f"你可以先使用 write_log 工具记录一些工作日志。"
                )

            log_parts = []
            for log in logs:
                log_parts.append(
                    f"## {log['date']} ({log['weekday']})\n\n{log['content'][:2000]}"
                )
            logs_text = "\n\n---\n\n".join(log_parts)

            return ToolResponse(
                content=(
                    f"最近 {len(logs)} 天的日志已读取：\n\n"
                    f"{logs_text}\n\n"
                    f"---\n接下来请使用 generate_weekly_plan 生成下周规划。"
                )
            )
        except Exception as e:
            return ToolResponse(content=f"读取日志出错: {str(e)}")

    @toolkit.register_tool_function
    def write_log(content: str) -> ToolResponse:
        """记录一条工作日志（追加到当天的 Markdown 日志文件中）。
        
        Args:
            content: 日志内容（支持 Markdown 格式）
        """
        try:
            filepath = LogService.write_log(content)
            filename = os.path.basename(filepath)
            return ToolResponse(
                content=f"日志已记录！\n文件: {filename}\n位置: {filepath}"
            )
        except Exception as e:
            return ToolResponse(content=f"记录日志出错: {str(e)}")

    @toolkit.register_tool_function
    def generate_weekly_plan() -> ToolResponse:
        """根据最近一周的日志，生成"下周规划"建议。
        先调用 read_weekly_logs 读取日志，再调用此工具生成规划。"""
        try:
            logs = LogService.read_logs(7)
            if not logs:
                return ToolResponse(content="没有找到日志记录，无法生成规划。请先记录一些工作日志。")

            prompt = LogService.build_weekly_prompt(logs)
            return ToolResponse(
                content=(
                    f"--- 下周规划生成指令 ---\n"
                    f"{prompt}\n\n"
                    f"--- 请根据以上日志和提示词，生成完整的下周规划，并用 save_report 保存 ---"
                )
            )
        except Exception as e:
            return ToolResponse(content=f"生成规划出错: {str(e)}")

    @toolkit.register_tool_function
    def list_reports() -> ToolResponse:
        """列出所有已生成的研究报告文件。"""
        try:
            reports = ReportService.list_reports()
            plans = LogService.list_plans()
            lines = []
            if reports:
                lines.append("【研究报告】")
                for r in reports:
                    lines.append(f"  📄 {os.path.basename(r)}")
            if plans:
                if lines:
                    lines.append("")
                lines.append("【下周规划】")
                for p in plans:
                    lines.append(f"  📋 {os.path.basename(p)}")
            if not lines:
                return ToolResponse(content="暂未生成任何报告或规划。")
            return ToolResponse(content="\n".join(lines))
        except Exception as e:
            return ToolResponse(content=f"列出文件出错: {str(e)}")

    return toolkit
