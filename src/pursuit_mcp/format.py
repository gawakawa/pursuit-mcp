"""Format Pursuit search results for display."""

from .types import PursuitResult, FormatOutput, FormattedResult


def format(results: list[PursuitResult]) -> FormatOutput:
    """Format Pursuit search results as structured dict.

    Args:
        results: List of Pursuit search results

    Returns:
        Formatted results dictionary with results list and count
    """
    if not results:
        return {"results": [], "count": 0}

    formatted_results: list[FormattedResult] = []
    for result in results:
        formatted_result: FormattedResult = {}

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

    return {"results": formatted_results, "count": len(results)}
