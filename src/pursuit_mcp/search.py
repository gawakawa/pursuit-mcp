"""Pursuit API client for searching PureScript documentation."""

from typing import TypedDict, Any

import httpx


class PursuitResultInfo(TypedDict, total=False):
    """Information about a Pursuit search result."""

    tag: str  # "package", "module", or "declaration"
    contents: Any  # Varies depending on tag


class PursuitResult(TypedDict, total=False):
    """Single Pursuit search result."""

    package: str
    version: str
    markup: str
    text: str
    info: PursuitResultInfo
    url: str


BASE_URL = "https://pursuit.purescript.org/search"
DEFAULT_TIMEOUT = 10.0


async def search(
    query: str, limit: int = 10, timeout: float = DEFAULT_TIMEOUT
) -> list[PursuitResult]:
    """Search Pursuit for PureScript functions, types, and documentation.

    Args:
        query: Search query (function name, type signature, or keyword)
        limit: Maximum number of results to return (default: 10)
        timeout: Request timeout in seconds

    Returns:
        List of search results from Pursuit (limited to `limit` results)

    Raises:
        httpx.HTTPError: If the request fails
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            BASE_URL,
            params={"q": query},
            headers={"Accept": "application/json"},
            timeout=timeout,
        )
        response.raise_for_status()
        results = response.json()
        return results[:limit]
