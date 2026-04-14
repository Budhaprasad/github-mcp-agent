import asyncio
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()

TOKEN    = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
USERNAME = os.getenv("GITHUB_USERNAME")

async def run(task: str):
    client = MultiServerMCPClient(
        {
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": TOKEN
                },
                "transport": "stdio"
            }
        }
    )

    tools = await client.get_tools()
    print(f"\n✅ GitHub MCP connected — {len(tools)} tools\n")

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite-preview",
        temperature=0,
        max_retries=3,
        request_timeout=60
    )

    agent = create_react_agent(llm, tools)

    result = await agent.ainvoke({
        "messages": [
            {
                "role": "user",
                "content": f"""
                You are a senior DevOps engineer.
                GitHub username : {USERNAME}

                Task: {task}
                """
            }
        ]
    })

    final = result["messages"][-1].content

    print("\n" + "="*50)
    print("✅ RESULT")
    print("="*50)
    print(final)

def get_input():
    """Read multiline input — type DONE to submit"""
    print("\n🤖 GitHub AI Agent — Day 2")
    print("="*50)
    print(f"   User : {os.getenv('GITHUB_USERNAME')}")
    print("="*50)
    print("\nType your task below.")
    print("When done type DONE on a new line and press Enter\n")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "DONE":
            break
        lines.append(line)

    return "\n".join(lines)

if __name__ == "__main__":
    task = get_input()
    print(f"\n👉 Running task...\n")
    asyncio.run(run(task))
