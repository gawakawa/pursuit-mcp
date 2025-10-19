"""Type definitions for Pursuit API responses."""

from typing import TypedDict, Literal, Union


class PackageResultContents(TypedDict):
    """Contents of a PackageResult.

    The boolean indicates whether the package is deprecated.
    """

    deprecated: bool


class ModuleResultContents(TypedDict):
    """Contents of a ModuleResult.

    Contains the module name.
    """

    module_name: str


class DeclarationResultContents(TypedDict):
    """Contents of a DeclarationResult.

    Contains information about a function, type, or value declaration.
    """

    namespace: str
    module_name: str
    title: str
    type_signature: str | None


class PackageResult(TypedDict):
    """A Pursuit search result for a package."""

    tag: Literal["PackageResult"]
    contents: bool  # Deprecation status


class ModuleResult(TypedDict):
    """A Pursuit search result for a module."""

    tag: Literal["ModuleResult"]
    contents: str  # Module name


class DeclarationResult(TypedDict):
    """A Pursuit search result for a declaration (function, type, etc.)."""

    tag: Literal["DeclarationResult"]
    contents: list[str | None]  # [namespace, module_name, title, type_signature]


# Union type for all possible result info types
PursuitResultInfo = Union[PackageResult, ModuleResult, DeclarationResult]


class PursuitResult(TypedDict):
    """A single Pursuit search result.

    Represents a search result from the Pursuit API, which can be a package,
    module, or declaration (function, type, value, etc.).
    """

    package: str
    version: str
    markup: str  # HTML-formatted documentation
    text: str  # Plain text documentation
    info: PursuitResultInfo
    url: str  # Direct link to the documentation


class FormattedResult(TypedDict, total=False):
    """A formatted Pursuit search result.

    All fields are optional as the formatter only includes fields present
    in the original result.
    """

    package: str
    version: str
    docs: str  # Plain text documentation
    type: str  # Result type (package, module, declaration)
    url: str
    # Declaration-specific fields
    module: str  # Module name (for declaration and module types)
    title: str  # Function/type name (for declaration types)
    typeText: str | None  # Type signature (for declaration types)
    # Package-specific fields
    deprecated: bool  # Deprecation status (for package types)


class FormatOutput(TypedDict):
    """Output format for formatted search results."""

    results: list[FormattedResult]
    count: int
