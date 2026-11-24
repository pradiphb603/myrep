#from mcp.server.mcpserver import MCPServer
from mcp.server.fastmcp import FastMCP
import KLayoutCreateShape
import KlayoutReadGDS

mcp=FastMCP("MY_MCP")
#mcp=MCPServer("MY_MCP")


@mcp.tool()
def add(a:int, b:int) -> int:
    return a+b

@mcp.tool()
def subtract(a:int, b:int) -> int:
    return a-b

@mcp.tool()
async def CreateRectangles() -> None:
    KLayoutCreateShape.create_rectangles()
    print("Successfully created rectangles and saved to output.gds")

@mcp.tool()
async def CreateRoute() -> None:
    KLayoutCreateShape.create_route()
    print("Successfully created route and saved to output.gds")

@mcp.tool()
async def ReadGDS(fp: str) -> list[dict[str, int | str]]:
    return KlayoutReadGDS.read_gds_file(file_path=fp)

if __name__ == "__main__":
    #mcp.run()
    mcp.run(transport="streamable-http")
