import os
import asyncio
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient


async def run_agent(messages):

    # MCP server configuration
    mcp_client = MultiServerMCPClient(
        {
            "klayout": {
               "transport": "http",
               "url":"http://localhost:8000/mcp"
            },

        }
    )

    # Discover MCP tools
    tools = await mcp_client.get_tools()

    if not tools:
        raise RuntimeError("No MCP tools found!")

    # Initialize Ollama LLM
    llm = ChatOllama(
        model="beam:cloud",
        temperature=0
    )

    # Create LangChain agent
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="""
        You are an AI assistant for KLayout EDA automation.

        You can execute operations using available MCP tools.

        Instructions:
        1. Understand the user's request.
        2. Select the appropriate MCP tool.
        3. Execute the tool when required.
        4. Explain the result clearly.
        5. Never claim a tool executed successfully unless
           you received a successful tool result.
        """
    )

    # Execute agent
    result = await agent.ainvoke(
        {"messages": messages}
    )

    return result["messages"][-1].content, tools

