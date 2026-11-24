import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langchain.agents import create_agent


async def main():

    # 1. Connect to MCP servers
    client = MultiServerMCPClient(
        {
            "klayout": {
                "transport": "http",
                "url": "http://localhost:8000/mcp"
            }
        },
        tool_name_prefix=True
    )

    # 2. Discover MCP tools
    tools = await client.get_tools()

    # 3. Initialize local Ollama model
    llm = ChatOllama(
        model="beam:cloud",
        temperature=0
    )

    # 4. Create LangChain agent
    agent = create_agent(
        model=llm,
        tools=tools
    )

    # 5. Send request to agent
    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    #"content": "Read the GDS file and list all available layers. File name is output.gds"
                    "content": "CreateLayout"
                }
            ]
        }
    )
    #print(response)
    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())