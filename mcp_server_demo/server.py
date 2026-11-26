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
async def CreateRectangles(fp: str) -> None:
    KLayoutCreateShape.create_rectangles(outFile=fp)
    print("Successfully created rectangles and saved to output.gds")

@mcp.tool()
async def CreateRoute(fp: str, width=250) -> str:
    KLayoutCreateShape.create_route(outFile=fp, width=width)
    #print("Successfully created route and saved to output.gds")
    return f"Successfully created route and saved to {fp}"

@mcp.tool()
async def ReadGDS(fp: str) -> list[dict[str, int | str]]:
    return KlayoutReadGDS.read_gds_file(file_path=fp)

@mcp.tool()
async def OpenKLayout() -> str:
    KlayoutReadGDS.open_klayout()
    return "Successfully opened klayout"

@mcp.tool()
async def CloseKLayout() -> str:
    KlayoutReadGDS.close_klayout()
    return "Successfully closed klayout"

if __name__ == "__main__":
    #mcp.run()
    mcp.run(transport="streamable-http")
