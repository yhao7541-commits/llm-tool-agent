from agent import run_agent
import logging
logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Tool Agent (Qwen) | 输入 'exit' 退出")
    while True:
        try:
            q = input("\n你：").strip()
            if not q:
                continue
            if q.lower() in {"exit", "quit"}:
                break

            ans = run_agent(q)
            logging.info(f"Agent：{ans}")
        # 处理 Ctrl+C 退出
        except KeyboardInterrupt:
            logging.info("\n（检测到 Ctrl+C，退出）")
            break
        # 处理其他异常
        except Exception as e:
            # 这里不需要知道具体错在哪，只要不让程序崩
            logging.error("Agent：我刚才出了一点问题，请再试一次。")

