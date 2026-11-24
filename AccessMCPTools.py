import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():

    client = MultiServerMCPClient({
        "klayout": {
            "transport": "http",
            "url": "http://localhost:8000/mcp"
        }
    })

    tools = await client.get_tools()

    for tool in tools:
        print(tool.name)


if __name__ == "__main__":
    asyncio.run(main())

