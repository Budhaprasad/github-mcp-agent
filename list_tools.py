import asyncio
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
load_dotenv()

TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

async def list_tools():
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
    print(f"\n✅ Total GitHub MCP Tools: {len(tools)}")
    print("="*50)
    for i, tool in enumerate(tools, 1):
        print(f"\n{i}. {tool.name}")
        print(f"   {tool.description}")

if __name__ == "__main__":
    asyncio.run(list_tools())

python3 list_tools.py
