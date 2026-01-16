from typing import Dict, Any, List
import json

from llm_qwen import chat
from tools import tool_calc, tool_time

SYSTEM = """你是一个工具调用Agent。
你在内部可以进行推理，但最终输出中不要包含 thought。
你必须严格输出 JSON，格式如下（不要输出任何额外文本）：

{
  "action": {
    "name": "calc" | "time" | "final",
    "args": { ... }
  }
}

规则：
- 如果需要计算，使用 calc，args: {"expr": "..."}。
- 如果需要当前时间，使用 time，args: {"tz": "America/Los_Angeles"}（默认这个时区）。
- 如果不需要工具，直接 final，args: {"answer": "..."}。
"""
# 解析 JSON 字符串，返回 Dict[str, Any] 或 None
def parse_json(s: str) -> Dict[str, Any]:
    # try strict parse; if model adds junk, attempt to extract json block
    s = s.strip()
    try:
        return json.loads(s)
    except Exception:
        # crude extraction
        start = s.find("{")
        end = s.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(s[start:end+1])
        raise
def safe_parse_json(s: str):
    try:
        return parse_json(s)
    except Exception:
        return None
def run_agent(user_query: str, max_steps: int = 3) -> str:
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user_query},
    ]

    for _ in range(max_steps):
        raw = chat(messages)

        data = safe_parse_json(raw)
        if data is None:
            # 模型没按 JSON 输出：直接要求它重来一次（最小可行兜底）
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": "你刚才没有严格输出 JSON。请只输出 JSON，不要任何多余文字。"})
            continue

        action = (data.get("action") or {})
        name = action.get("name")
        args = action.get("args", {}) or {}

        if name == "final":
            return str(args.get("answer", "")).strip()

        # --- 工具执行兜底 ---
        try:
            if name == "calc":
                obs = tool_calc(str(args.get("expr", "")))
            elif name == "time":
                obs = tool_time(str(args.get("tz", "America/Los_Angeles")))
            else:
                obs = {"ok": False, "error": f"Unknown action: {name}"}
        except Exception as e:
            obs = {"ok": False, "error": f"Tool error: {e}"}

        messages.append({"role": "assistant", "content": raw})
        messages.append({"role": "user", "content": f"工具返回结果如下（请继续严格输出 JSON）：\n{json.dumps(obs, ensure_ascii=False)}"})

    return "抱歉，我没有在限定步数内完成任务。"


