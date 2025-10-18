"""Format Pursuit search results for display."""

from .search import PursuitResult


def format(results: list[PursuitResult]) -> str:
    """Format Pursuit search results as JSON string.

    Args:
        results: List of Pursuit search results

    Returns:
        JSON string representation of results
    """
    import json

    if not results:
        return json.dumps({"results": [], "count": 0})

    formatted_results = []
    for result in results:
        formatted_result = {}

        # Package and version information
        if "package" in result:
            formatted_result["package"] = result["package"]

        if "version" in result:
            formatted_result["version"] = result["version"]

        # Documentation text
        if "text" in result:
            formatted_result["docs"] = result["text"]

        # Result info (package/module/declaration)
        if "info" in result:
            info = result["info"]
            if isinstance(info, dict) and "tag" in info:
                formatted_result["type"] = info["tag"]
                if "contents" in info:
                    formatted_result["contents"] = info["contents"]

        # URL to the result
        if "url" in result:
            formatted_result["url"] = result["url"]

        formatted_results.append(formatted_result)

    return json.dumps(
        {"results": formatted_results, "count": len(results)}, ensure_ascii=False
    )
