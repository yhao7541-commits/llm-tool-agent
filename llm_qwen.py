# 这个文件负责：把一句话发给通义千问，再拿回回答
from typing import List, Dict, Any
import dashscope
from dashscope import Generation

from config import DASHSCOPE_API_KEY, ensure_config

def chat(messages, model: str = "qwen-turbo") -> str:
    ensure_config()
    dashscope.api_key = DASHSCOPE_API_KEY

    try:
        resp = Generation.call(
            model=model,
            messages=messages,
            result_format="message",
            temperature=0.2,
        )
    except Exception as e:
        raise RuntimeError(f"LLM call failed: {e}")

    try:
        return resp.output["choices"][0]["message"]["content"]
    except Exception:
        raise RuntimeError(f"Unexpected DashScope response shape: {resp}")