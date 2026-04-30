# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Optional

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    raw: dict = field(default_factory=dict, repr=False)


class SearchService:
    """网络搜索服务。

    封装搜索引擎调用，支持多后端扩展。
    当前默认使用 DuckDuckGo（免费无需 API Key），
    后续可扩展 Google CSE / Bing / Tavily / MCP 等后端。
    """

    def __init__(self, engine: str = "duckduckgo", api_key: Optional[str] = None):
        self._engine = engine
        self._api_key = api_key

    def search(self, query: str, max_results: int = 5) -> list[SearchResult]:
        if self._engine == "duckduckgo":
            return self._search_duckduckgo(query, max_results)
        raise ValueError(f"不支持的搜索引擎: {self._engine}")

    def _search_duckduckgo(self, query: str, max_results: int) -> list[SearchResult]:
        results = []
        with DDGS() as ddgs:
            raw_results = list(ddgs.text(query, max_results=max_results))
        for r in raw_results:
            results.append(
                SearchResult(
                    title=r.get("title", "无标题"),
                    url=r.get("href", ""),
                    snippet=r.get("body", "无摘要"),
                    raw=r,
                )
            )
        return results

    def fetch_page(self, url: str, max_chars: int = 8000) -> str:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding

        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        text = "\n".join(lines)

        if len(text) > max_chars:
            text = text[:max_chars] + "\n\n... [内容已截断]"
        return text or "(未能提取到文本内容)"

    @staticmethod
    def format_results(results: list[SearchResult]) -> str:
        if not results:
            return "未找到相关搜索结果。"
        lines = []
        for i, r in enumerate(results, 1):
            lines.append(f"[{i}] {r.title}\n    URL: {r.url}\n    摘要: {r.snippet}")
        return "\n\n".join(lines)
