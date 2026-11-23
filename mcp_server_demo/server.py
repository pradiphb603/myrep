#from mcp.server.mcpserver import MCPServer
from mcp.server.fastmcp import FastMCP
import kl
import Read

mcp=FastMCP("MY_MCP")


@mcp.tool()
def add(a:int, b:int) -> int:
    return a+b

@mcp.tool()
def subtract(a:int, b:int) -> int:
    return a-b

@mcp.tool()
async def CreateLayout() -> None:
    kl.create_layout()
    print("Successfully created layout and saved to output.gds")

@mcp.tool()
async def CreateRoute() -> None:
    kl.create_route()
    print("Successfully created route and saved to output.gds")

@mcp.tool()
async def ReadGDS(fp: str) -> list[dict[str, int | str]]:
    return Read.read_gds_file(file_path=fp)

if __name__ == "__main__":
    #mcp.run()
    mcp.run(transport="streamable-http")
