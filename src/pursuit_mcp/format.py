"""Format Pursuit search results for display."""

from typing import cast

from .types import (
    PursuitResult,
    FormatOutput,
    FormattedResult,
    DeclarationResult,
    ModuleResult,
    PackageResult,
)


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
            result_type = info["type"]
            formatted_result["type"] = result_type

            # Extract type-specific information
            if result_type == "declaration":
                decl_info = cast(DeclarationResult, info)
                formatted_result["module"] = decl_info["module"]
                formatted_result["title"] = decl_info["title"]
                if "typeText" in decl_info:
                    formatted_result["typeText"] = decl_info["typeText"]
            elif result_type == "module":
                mod_info = cast(ModuleResult, info)
                formatted_result["module"] = mod_info["module"]
            elif result_type == "package":
                pkg_info = cast(PackageResult, info)
                formatted_result["deprecated"] = pkg_info["deprecated"]

        # URL to the result
        if "url" in result:
            formatted_result["url"] = result["url"]

        formatted_results.append(formatted_result)

    return {"results": formatted_results, "count": len(results)}
