from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

mcp = FastMCP(
    name="Tiktok MCP Server",
    version="1.0.0",
    instructions="Use this server to interact with Tiktok API.",
    tools=[],
    include_tags=["tiktok", "social media", "api"],
    exclude_tags=["deprecated", "internal"],
    on_duplicate_prompts="ignore",
    include_fastmcp_meta=True,
)


# TOOLS
@mcp.tool
async def greet(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool
async def sum(a: int, b: int) -> int:
    """Sums two integers."""
    return a + b


# RESOURCES
@mcp.resource("data://config")
async def get_config() -> dict:
    return {"api_key": "your_api_key", "api_secret": "your_api_secret"}


@mcp.resource("users://{user_id}/profile")
async def get_user_profile(user_id: str) -> dict:
    # Mock user profile data
    return {"user_id": user_id, "name": "John Doe", "followers": 1500}


# CUSTOM ROUTES
@mcp.custom_route("/status", methods=["GET"])
async def status(request: Request):
    return JSONResponse(content={"status": "ok", "message": "Tiktok MCP Server is running."})

@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request):
    return JSONResponse(content={"status": "healthy"})


# PROMPTS
@mcp.prompt
async def analyze_user_profile(user_id: str) -> str:
    profile = await get_user_profile(user_id)
    return f"User {profile['name']} has {profile['followers']} followers."

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)