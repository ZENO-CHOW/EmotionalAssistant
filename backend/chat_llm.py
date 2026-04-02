#!/usr/bin/env python3
"""
LLM 交互式对话脚本
可直接与 LLM 对话，方便调试和测试

用法:
    python chat_llm.py
    python chat_llm.py --model "ZhipuAI/GLM-4.7-Flash"
    python chat_llm.py --system "你是一个心理助手"
"""

import sys
from pathlib import Path
from typing import List, Optional

backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from dotenv import load_dotenv

load_dotenv(backend_dir / ".env")

from app.core.llm_client import LLMClient
from app.config import settings


def print_banner():
    print("\n" + "=" * 60)
    print("  LLM 交互式对话终端")
    print("=" * 60)
    print(f"  模型: {settings.LLM_MODEL}")
    print(f"  Base URL: {settings.LLM_BASE_URL}")
    print(f"  Temperature: {settings.LLM_TEMPERATURE}")
    print(f"  Max Tokens: {settings.LLM_MAX_TOKENS}")
    print("-" * 60)
    print("  命令:")
    print("    /system <提示词>  - 设置系统提示词")
    print("    /clear            - 清除对话历史")
    print("    /history          - 查看对话历史")
    print("    /quit 或 /exit    - 退出")
    print("    /help             - 显示帮助")
    print("-" * 60)
    print()


def print_help():
    print("\n=== 帮助 ===")
    print("直接输入内容与 LLM 对话")
    print("特殊命令（以 / 开头）:")
    print("  /system <text>  - 设置系统提示词")
    print("  /clear          - 清除对话历史")
    print("  /history        - 显示对话历史")
    print("  /quit           - 退出程序")
    print()


class LLMTerminal:
    def __init__(self, system_prompt: Optional[str] = None):
        self.client = LLMClient()
        self.system_prompt = (
            system_prompt or "你是一个专业的心理助手，善于倾听和提供支持。"
        )
        self.conversation_history: List[dict] = []

    def clear_history(self):
        """清除对话历史"""
        self.conversation_history = []
        print("✓ 对话历史已清除\n")

    def show_history(self):
        """显示对话历史"""
        if not self.conversation_history:
            print("对话历史为空\n")
            return

        print("\n--- 对话历史 ---")
        for i, msg in enumerate(self.conversation_history):
            role = msg["role"].upper()
            content = msg["content"]
            if len(content) > 100:
                content = content[:100] + "..."
            print(f"[{i + 1}] {role}: {content}")
        print("---\n")

    def chat(self, message: str) -> str:
        """发送消息并获取回复"""
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history[-20:])
        messages.append({"role": "user", "content": message})

        response = self.client.generate_response(
            system_prompt=self.system_prompt,
            user_message=message,
            context={"conversation_turns": len(self.conversation_history) // 2 + 1},
        )

        self.conversation_history.append({"role": "user", "content": message})
        self.conversation_history.append({"role": "assistant", "content": response})

        return response

    def chat_stream(self, message: str):
        """流式对话"""
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history[-20:])
        messages.append({"role": "user", "content": message})

        print("LLM: ", end="", flush=True)

        for chunk in self.client.stream_chat(messages):
            print(chunk, end="", flush=True)
        print("\n")

        self.conversation_history.append({"role": "user", "content": message})
        full_response = ""
        for chunk in self.client.stream_chat(messages):
            full_response += chunk
        self.conversation_history.append(
            {"role": "assistant", "content": full_response}
        )

    def run(self):
        """运行交互式对话"""
        print_banner()

        while True:
            try:
                user_input = input("你: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n\n再见！")
                break

            if not user_input:
                continue

            if user_input.lower() in ["/quit", "/exit", "/q"]:
                print("再见！")
                break

            if user_input.lower() == "/help":
                print_help()
                continue

            if user_input.startswith("/system"):
                parts = user_input[8:].strip()
                if parts:
                    self.system_prompt = parts
                    print(f"✓ 系统提示词已更新: {parts[:50]}...\n")
                else:
                    print(f"当前系统提示词: {self.system_prompt}\n")
                continue

            if user_input.lower() == "/clear":
                self.clear_history()
                continue

            if user_input.lower() == "/history":
                self.show_history()
                continue

            try:
                print()
                response = self.chat(user_input)
                print(f"LLM: {response}\n")
            except Exception as e:
                print(f"\n❌ 错误: {e}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="LLM 交互式对话终端")
    parser.add_argument("--model", "-m", default=None, help="指定模型名称")
    parser.add_argument("--system", "-s", default=None, help="设置系统提示词")
    parser.add_argument("--stream", action="store_true", help="使用流式输出")
    args = parser.parse_args()

    if args.model:
        print(f"注意: 模型覆盖仅在本次会话有效 ({args.model})")

    terminal = LLMTerminal(system_prompt=args.system)
    terminal.run()


if __name__ == "__main__":
    main()
