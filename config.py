# -*- coding: utf-8 -*-
import os
import sys

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)
PPT_DIR = os.path.join(PROJECT_ROOT, "ppts")
os.makedirs(PPT_DIR, exist_ok=True)
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

PROVIDERS = ["ollama", "dashscope", "openai", "gemini", "deepseek", "custom"]


def get_model_config():
    provider = os.getenv("LLM_PROVIDER", "").strip().lower()

    if provider == "ollama":
        return _ollama_config()
    elif provider == "dashscope":
        return _dashscope_config()
    elif provider == "openai":
        return _openai_config()
    elif provider == "gemini":
        return _gemini_config()
    elif provider == "deepseek":
        return _deepseek_config()
    elif provider == "custom":
        return _custom_config()
    elif not provider:
        return _auto_detect()
    else:
        print(f"[ERROR] 不支持的 LLM_PROVIDER: {provider}")
        print(f"  支持的选项: {', '.join(PROVIDERS)}")
        sys.exit(1)


def _ollama_config():
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "qwen3")
    print(f"[INFO] 使用 Ollama 本地模型: {model} @ {host}")
    return {
        "provider": "ollama",
        "model_name": model,
        "host": host,
    }


def _dashscope_config():
    api_key = _require_env("DASHSCOPE_API_KEY")
    model = os.getenv("DASHSCOPE_MODEL", "qwen-max")
    return {
        "provider": "dashscope",
        "model_name": model,
        "api_key": api_key,
    }


def _openai_config():
    api_key = _require_env("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o")
    base_url = os.getenv("OPENAI_BASE_URL") or None
    return {
        "provider": "openai",
        "model_name": model,
        "api_key": api_key,
        "base_url": base_url,
    }


def _gemini_config():
    api_key = _require_env("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    return {
        "provider": "gemini",
        "model_name": model,
        "api_key": api_key,
    }


def _deepseek_config():
    api_key = _require_env("DEEPSEEK_API_KEY")
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    return {
        "provider": "deepseek",
        "model_name": model,
        "api_key": api_key,
        "base_url": base_url,
    }


def _custom_config():
    api_key = _require_env("CUSTOM_API_KEY")
    model = _require_env("CUSTOM_MODEL")
    base_url = _require_env("CUSTOM_BASE_URL")
    provider_info = os.getenv("CUSTOM_PROVIDER_NAME", model)
    return {
        "provider": "custom",
        "model_name": model,
        "api_key": api_key,
        "base_url": base_url,
        "provider_info": provider_info,
    }


def _auto_detect():
    if os.getenv("OLLAMA_HOST") or os.getenv("OLLAMA_MODEL"):
        return _ollama_config()
    if os.getenv("DASHSCOPE_API_KEY"):
        return _dashscope_config()
    if os.getenv("GEMINI_API_KEY"):
        return _gemini_config()
    if os.getenv("DEEPSEEK_API_KEY"):
        return _deepseek_config()
    if os.getenv("CUSTOM_API_KEY") and os.getenv("CUSTOM_BASE_URL"):
        return _custom_config()
    if os.getenv("OPENAI_API_KEY"):
        return _openai_config()

    _error_no_config()


def _require_env(key: str) -> str:
    value = os.getenv(key, "").strip()
    if not value:
        print(f"[ERROR] 缺少必需的环境变量: {key}")
        print("请在 .env 文件或系统环境变量中设置。")
        sys.exit(1)
    return value


def _error_no_config():
    print("[ERROR] 未检测到任何模型配置！")
    print()
    print("请设置 LLM_PROVIDER 环境变量来选择模型提供方，或在 .env 中配置以下之一：")
    print()
    print("  本地模型（免费，无需 API Key）：")
    print("    LLM_PROVIDER=ollama")
    print("    OLLAMA_MODEL=qwen3")
    print("    OLLAMA_HOST=http://localhost:11434")
    print()
    print("  云端模型（需要 API Key）：")
    print("    LLM_PROVIDER=dashscope   # 通义千问")
    print("    LLM_PROVIDER=openai      # OpenAI / 兼容接口")
    print("    LLM_PROVIDER=gemini      # Google Gemini")
    print("    LLM_PROVIDER=deepseek    # DeepSeek")
    print("    LLM_PROVIDER=custom      # 自定义 OpenAI 兼容 API")
    print()
    print("详见 .env.example 文件。")
    sys.exit(1)
