from fastmcp import FastMCP

mcp = FastMCP("Pursuit Search")


@mcp.tool
async def search_pursuit(query: str, limit: int = 10) -> str:
    """Search Pursuit for PureScript functions, types, and documentation.

    Args:
        query: Search query (function name, type signature, or keyword)
        limit: Maximum number of results to return (default: 10)

    Returns:
        Formatted search results from Pursuit
    """
    from .format import format
    from .search import search

    results = await search(query, limit=limit)
    return format(results)


if __name__ == "__main__":
    mcp.run()
