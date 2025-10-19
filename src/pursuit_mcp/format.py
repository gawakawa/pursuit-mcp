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
            if isinstance(info, dict) and "type" in info:
                result_type = info["type"]
                formatted_result["type"] = result_type

                # Extract type-specific information
                if result_type == "declaration":
                    # For declarations, include module, title, and typeText
                    if "module" in info:
                        formatted_result["module"] = info["module"]
                    if "title" in info:
                        formatted_result["title"] = info["title"]
                    if "typeText" in info:
                        formatted_result["typeText"] = info["typeText"]
                elif result_type == "module":
                    # For modules, include module name
                    if "module" in info:
                        formatted_result["module"] = info["module"]
                elif result_type == "package":
                    # For packages, include deprecated status
                    if "deprecated" in info:
                        formatted_result["deprecated"] = info["deprecated"]

        # URL to the result
        if "url" in result:
            formatted_result["url"] = result["url"]

        formatted_results.append(formatted_result)

    return {"results": formatted_results, "count": len(results)}
