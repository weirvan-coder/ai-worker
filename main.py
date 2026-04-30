# -*- coding: utf-8 -*-
import asyncio

from agentscope.message import Msg

from agent.friday_agent import create_agent


async def chat_loop():
    agent = create_agent()

    print("\n" + "=" * 60)
    print("  🔍 Friday 研究助手 - 基于 AgentScope")
    print("  我能帮你搜索网络并生成 Markdown 研究报告")
    print("  输入 'exit' 退出对话，输入 'reports' 查看已生成报告")
    print("=" * 60 + "\n")

    msg = None
    while True:
        try:
            user_input = input("🧑 你: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 再见！")
            break

        if not user_input:
            continue
        if user_input.lower() == "exit":
            print("👋 再见！")
            break
        if user_input.lower() == "reports":
            from services.report_service import ReportService
            reports = ReportService.list_reports()
            if reports:
                print(f"\n📄 已有 {len(reports)} 份报告:")
                for r in reports:
                    print(f"  • {r}")
            else:
                print("\n� 暂未生成任何报告。")
            print()
            continue

        msg = Msg("user", user_input, role="user")
        print("\n🤖 Friday 思考中...\n")

        try:
            response = await agent(msg)
            content = response.get_text_content()
            print(f"🤖 Friday:\n{content}\n")
        except Exception as e:
            print(f"[ERROR] 智能体运行出错: {e}\n")


def main():
    asyncio.run(chat_loop())


if __name__ == "__main__":
    main()
