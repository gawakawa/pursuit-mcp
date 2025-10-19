"""Unit tests for format module."""

from pursuit_mcp.format import format
from pursuit_mcp.types import PursuitResult, FormatOutput


def test_format_empty_results():
    """Test formatting empty results list."""
    input_data: list[PursuitResult] = []
    expected: FormatOutput = {"results": [], "count": 0}
    assert format(input_data) == expected


def test_format_package_result():
    """Test formatting a PackageResult."""
    input_data: list[PursuitResult] = [
        {
            "package": "purescript-prelude",
            "version": "6.0.1",
            "markup": "<p>Core library</p>",
            "text": "Core library",
            "info": {
                "tag": "PackageResult",
                "contents": False,
            },
            "url": "https://pursuit.purescript.org/packages/purescript-prelude",
        }
    ]
    expected: FormatOutput = {
        "results": [
            {
                "package": "purescript-prelude",
                "version": "6.0.1",
                "docs": "Core library",
                "type": "PackageResult",
                "contents": False,
                "url": "https://pursuit.purescript.org/packages/purescript-prelude",
            }
        ],
        "count": 1,
    }
    assert format(input_data) == expected


def test_format_module_result():
    """Test formatting a ModuleResult."""
    input_data: list[PursuitResult] = [
        {
            "package": "purescript-prelude",
            "version": "6.0.1",
            "markup": "<p>Array operations</p>",
            "text": "Array operations",
            "info": {
                "tag": "ModuleResult",
                "contents": "Data.Array",
            },
            "url": "https://pursuit.purescript.org/packages/purescript-prelude/docs/Data.Array",
        }
    ]
    expected: FormatOutput = {
        "results": [
            {
                "package": "purescript-prelude",
                "version": "6.0.1",
                "docs": "Array operations",
                "type": "ModuleResult",
                "contents": "Data.Array",
                "url": "https://pursuit.purescript.org/packages/purescript-prelude/docs/Data.Array",
            }
        ],
        "count": 1,
    }
    assert format(input_data) == expected


def test_format_declaration_result():
    """Test formatting a DeclarationResult."""
    input_data: list[PursuitResult] = [
        {
            "package": "purescript-prelude",
            "version": "6.0.1",
            "markup": "<p>Map function</p>",
            "text": "Map function",
            "info": {
                "tag": "DeclarationResult",
                "contents": ["value", "Data.Functor", "map", "(a -> b) -> f a -> f b"],
            },
            "url": "https://pursuit.purescript.org/packages/purescript-prelude/docs/Data.Functor#v:map",
        }
    ]
    expected: FormatOutput = {
        "results": [
            {
                "package": "purescript-prelude",
                "version": "6.0.1",
                "docs": "Map function",
                "type": "DeclarationResult",
                "contents": ["value", "Data.Functor", "map", "(a -> b) -> f a -> f b"],
                "url": "https://pursuit.purescript.org/packages/purescript-prelude/docs/Data.Functor#v:map",
            }
        ],
        "count": 1,
    }
    assert format(input_data) == expected


def test_format_multiple_results():
    """Test formatting multiple results."""
    input_data: list[PursuitResult] = [
        {
            "package": "purescript-prelude",
            "version": "6.0.1",
            "markup": "<p>Package</p>",
            "text": "Package",
            "info": {
                "tag": "PackageResult",
                "contents": False,
            },
            "url": "https://pursuit.purescript.org/packages/purescript-prelude",
        },
        {
            "package": "purescript-arrays",
            "version": "7.0.0",
            "markup": "<p>Module</p>",
            "text": "Module",
            "info": {
                "tag": "ModuleResult",
                "contents": "Data.Array",
            },
            "url": "https://pursuit.purescript.org/packages/purescript-arrays/docs/Data.Array",
        },
    ]
    expected: FormatOutput = {
        "results": [
            {
                "package": "purescript-prelude",
                "version": "6.0.1",
                "docs": "Package",
                "type": "PackageResult",
                "contents": False,
                "url": "https://pursuit.purescript.org/packages/purescript-prelude",
            },
            {
                "package": "purescript-arrays",
                "version": "7.0.0",
                "docs": "Module",
                "type": "ModuleResult",
                "contents": "Data.Array",
                "url": "https://pursuit.purescript.org/packages/purescript-arrays/docs/Data.Array",
            },
        ],
        "count": 2,
    }
    assert format(input_data) == expected


def test_format_declaration_with_null_type():
    """Test formatting a DeclarationResult with null type signature."""
    input_data: list[PursuitResult] = [
        {
            "package": "purescript-prelude",
            "version": "6.0.1",
            "markup": "<p>Some declaration</p>",
            "text": "Some declaration",
            "info": {
                "tag": "DeclarationResult",
                "contents": ["value", "Data.Module", "something", None],
            },
            "url": "https://pursuit.purescript.org/packages/purescript-prelude/docs/Data.Module#v:something",
        }
    ]
    expected: FormatOutput = {
        "results": [
            {
                "package": "purescript-prelude",
                "version": "6.0.1",
                "docs": "Some declaration",
                "type": "DeclarationResult",
                "contents": ["value", "Data.Module", "something", None],
                "url": "https://pursuit.purescript.org/packages/purescript-prelude/docs/Data.Module#v:something",
            }
        ],
        "count": 1,
    }
    assert format(input_data) == expected
