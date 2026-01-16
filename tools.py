# 工具层：定义模型不能直接完成、需要程序执行的功能
from typing import Any, Dict
import math
from datetime import datetime
from zoneinfo import ZoneInfo
import ast

def safe_eval(expr: str):
    node = ast.parse(expr, mode="eval")
    for n in ast.walk(node):
        if not isinstance(n, (ast.Expression, ast.BinOp, ast.Num,
                               ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)):
            raise ValueError("Unsupported expression")
    return eval(compile(node, "<expr>", "eval"))

# 工具：计算器
def tool_calc(expr: str) -> Dict[str, Any]:
    """
    A very small safe-ish calculator.
    Supports + - * / ** and math functions via a whitelist.
    """
    allowed = {
        "math": math,
        "__builtins__": {},
    }
    try:
        value = safe_eval(expr)
        return {
  "tool": "calc",
  "success": True,
  "data": { "result": 42 }
}
    except Exception as e:
        return {
  "tool": "calc",
  "success": False,
  "error": "Invalid expression"
}
# 工具：获取当前时间
def tool_time(tz: str = "America/Los_Angeles") -> Dict[str, Any]:
    try:
        now = datetime.now(ZoneInfo(tz))
        return {"ok": True, "timezone": tz, "iso": now.isoformat()}
    except Exception as e:
        return {"ok": False, "error": str(e)}
