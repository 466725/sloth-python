import asyncio
from starlette.requests import Request
from starlette.responses import Response
from mcp.server.fastmcp import FastMCP, Context


mcp = FastMCP(
    "mcp-server",
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
async def add(a: int, b: int, ctx: Context) -> int:
    await ctx.info("Preparing to add...")
    await asyncio.sleep(2)
    await ctx.report_progress(80, 100)

    return a + b


# Load the demo HTML page
@mcp.custom_route("/", methods=["GET"])
async def get(request: Request) -> Response:
    with open("index.html", "r") as f:
        html_content = f.read()
    return Response(content=html_content, media_type="text/html")


mcp.run(transport="streamable-http")
