# 配置管理：读取 .env 中的 API Key 等配置
# 从 .env 文件中读取 DASHSCOPE_API_KEY
import os
from dotenv import load_dotenv

load_dotenv()

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "").strip()

def ensure_config() -> None:
    if not DASHSCOPE_API_KEY:
        raise RuntimeError(
            "Missing DASHSCOPE_API_KEY. "
            "Set environment variable DASHSCOPE_API_KEY or create a .env file."
        )
