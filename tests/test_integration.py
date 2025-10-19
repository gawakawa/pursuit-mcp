"""Integration tests for API response and formatting."""

import pytest
from pytest_httpx import HTTPXMock

from pursuit_mcp.search import search
from pursuit_mcp.format import format
from pursuit_mcp.types import FormatOutput


@pytest.mark.asyncio
async def test_search_and_format_function_results(httpx_mock: HTTPXMock):
    """Test integration of search API and format for function results."""
    # Mock API response for 'map' function
    api_response = [
        {
            "info": {
                "module": "Data.Functor",
                "title": "map",
                "type": "declaration",
                "typeOrValue": "ValueLevel",
                "typeText": "forall f a b. Functor f => (a -> b) -> f a -> f b",
            },
            "markup": "<p>Map function</p>\n",
            "package": "purescript-prelude",
            "text": "Map function\n",
            "url": "https://pursuit.purescript.org/packages/purescript-prelude/6.0.2/docs/Data.Functor#v:map",
            "version": "6.0.2",
        },
        {
            "info": {
                "module": "Data.Set",
                "title": "map",
                "type": "declaration",
                "typeOrValue": "ValueLevel",
                "typeText": "forall a b. Ord b => (a -> b) -> Set a -> Set b",
            },
            "markup": "<p>Maps over the values in a set.</p>\n",
            "package": "purescript-ordered-collections",
            "text": "Maps over the values in a set.\n",
            "url": "https://pursuit.purescript.org/packages/purescript-ordered-collections/3.2.0/docs/Data.Set#v:map",
            "version": "3.2.0",
        },
    ]
    httpx_mock.add_response(json=api_response)

    # Search for results
    search_results = await search("map", limit=2)

    # Format the results
    formatted = format(search_results)

    # Expected formatted output
    expected: FormatOutput = {
        "results": [
            {
                "package": "purescript-prelude",
                "version": "6.0.2",
                "docs": "Map function\n",
                "type": "declaration",
                "url": "https://pursuit.purescript.org/packages/purescript-prelude/6.0.2/docs/Data.Functor#v:map",
            },
            {
                "package": "purescript-ordered-collections",
                "version": "3.2.0",
                "docs": "Maps over the values in a set.\n",
                "type": "declaration",
                "url": "https://pursuit.purescript.org/packages/purescript-ordered-collections/3.2.0/docs/Data.Set#v:map",
            },
        ],
        "count": 2,
    }

    assert formatted == expected


@pytest.mark.asyncio
async def test_search_and_format_module_results(httpx_mock: HTTPXMock):
    """Test integration of search API and format for module results."""
    # Mock API response for 'Data.Array' module
    api_response = [
        {
            "info": {"module": "Data.Array", "type": "module"},
            "markup": "<p>Helper functions for working with immutable Javascript arrays.</p>\n",
            "package": "purescript-arrays",
            "text": "Helper functions for working with immutable Javascript arrays.\n",
            "url": "https://pursuit.purescript.org/packages/purescript-arrays/7.3.0/docs/Data.Array",
            "version": "7.3.0",
        },
        {
            "info": {"module": "Data.Array.ST", "type": "module"},
            "markup": "<p>Helper functions for working with mutable arrays using the ST effect.</p>\n",
            "package": "purescript-arrays",
            "text": "Helper functions for working with mutable arrays using the ST effect.\n",
            "url": "https://pursuit.purescript.org/packages/purescript-arrays/7.3.0/docs/Data.Array.ST",
            "version": "7.3.0",
        },
    ]
    httpx_mock.add_response(json=api_response)

    # Search for results
    search_results = await search("Data.Array", limit=2)

    # Format the results
    formatted = format(search_results)

    # Expected formatted output
    expected: FormatOutput = {
        "results": [
            {
                "package": "purescript-arrays",
                "version": "7.3.0",
                "docs": "Helper functions for working with immutable Javascript arrays.\n",
                "type": "module",
                "url": "https://pursuit.purescript.org/packages/purescript-arrays/7.3.0/docs/Data.Array",
            },
            {
                "package": "purescript-arrays",
                "version": "7.3.0",
                "docs": "Helper functions for working with mutable arrays using the ST effect.\n",
                "type": "module",
                "url": "https://pursuit.purescript.org/packages/purescript-arrays/7.3.0/docs/Data.Array.ST",
            },
        ],
        "count": 2,
    }

    assert formatted == expected


@pytest.mark.asyncio
async def test_search_and_format_package_results(httpx_mock: HTTPXMock):
    """Test integration of search API and format for package results."""
    # Mock API response for 'prelude' package
    api_response = [
        {
            "info": {"deprecated": False, "type": "package"},
            "markup": "<p>The PureScript Prelude</p>\n",
            "package": "purescript-prelude",
            "text": "The PureScript Prelude\n",
            "url": "https://pursuit.purescript.org/packages/purescript-prelude",
            "version": "6.0.2",
        }
    ]
    httpx_mock.add_response(json=api_response)

    # Search for results
    search_results = await search("prelude", limit=1)

    # Format the results
    formatted = format(search_results)

    # Expected formatted output
    expected: FormatOutput = {
        "results": [
            {
                "package": "purescript-prelude",
                "version": "6.0.2",
                "docs": "The PureScript Prelude\n",
                "type": "package",
                "url": "https://pursuit.purescript.org/packages/purescript-prelude",
            }
        ],
        "count": 1,
    }

    assert formatted == expected


@pytest.mark.asyncio
async def test_search_and_format_empty_results(httpx_mock: HTTPXMock):
    """Test integration of search API and format with no results."""
    # Mock API response with empty results
    api_response = []
    httpx_mock.add_response(json=api_response)

    # Search for results
    search_results = await search("nonexistent", limit=10)

    # Format the results
    formatted = format(search_results)

    # Expected formatted output
    expected: FormatOutput = {"results": [], "count": 0}

    assert formatted == expected


@pytest.mark.asyncio
async def test_search_and_format_mixed_result_types(httpx_mock: HTTPXMock):
    """Test integration of search API and format with mixed result types."""
    # Mock API response with package, module, and declaration
    api_response = [
        {
            "info": {"deprecated": False, "type": "package"},
            "markup": "<p>The PureScript Prelude</p>\n",
            "package": "purescript-prelude",
            "text": "The PureScript Prelude\n",
            "url": "https://pursuit.purescript.org/packages/purescript-prelude",
            "version": "6.0.2",
        },
        {
            "info": {"module": "Prelude", "type": "module"},
            "markup": "<p>Core module</p>\n",
            "package": "purescript-prelude",
            "text": "Core module\n",
            "url": "https://pursuit.purescript.org/packages/purescript-prelude/6.0.2/docs/Prelude",
            "version": "6.0.2",
        },
        {
            "info": {
                "module": "Data.Functor",
                "title": "map",
                "type": "declaration",
                "typeOrValue": "ValueLevel",
                "typeText": "forall f a b. Functor f => (a -> b) -> f a -> f b",
            },
            "markup": "<p>Map function</p>\n",
            "package": "purescript-prelude",
            "text": "Map function\n",
            "url": "https://pursuit.purescript.org/packages/purescript-prelude/6.0.2/docs/Data.Functor#v:map",
            "version": "6.0.2",
        },
    ]
    httpx_mock.add_response(json=api_response)

    # Search for results
    search_results = await search("prelude", limit=3)

    # Format the results
    formatted = format(search_results)

    # Expected formatted output
    expected: FormatOutput = {
        "results": [
            {
                "package": "purescript-prelude",
                "version": "6.0.2",
                "docs": "The PureScript Prelude\n",
                "type": "package",
                "url": "https://pursuit.purescript.org/packages/purescript-prelude",
            },
            {
                "package": "purescript-prelude",
                "version": "6.0.2",
                "docs": "Core module\n",
                "type": "module",
                "url": "https://pursuit.purescript.org/packages/purescript-prelude/6.0.2/docs/Prelude",
            },
            {
                "package": "purescript-prelude",
                "version": "6.0.2",
                "docs": "Map function\n",
                "type": "declaration",
                "url": "https://pursuit.purescript.org/packages/purescript-prelude/6.0.2/docs/Data.Functor#v:map",
            },
        ],
        "count": 3,
    }

    assert formatted == expected


@pytest.mark.asyncio
async def test_search_and_format_with_limit(httpx_mock: HTTPXMock):
    """Test integration respects limit parameter."""
    # Mock API response with more results than limit
    api_response = [
        {
            "info": {
                "module": "Data.Functor",
                "title": "map",
                "type": "declaration",
                "typeOrValue": "ValueLevel",
                "typeText": "forall f a b. Functor f => (a -> b) -> f a -> f b",
            },
            "markup": "<p>Map function</p>\n",
            "package": "purescript-prelude",
            "text": "Map function\n",
            "url": "https://pursuit.purescript.org/packages/purescript-prelude/6.0.2/docs/Data.Functor#v:map",
            "version": "6.0.2",
        },
        {
            "info": {
                "module": "Data.Set",
                "title": "map",
                "type": "declaration",
                "typeOrValue": "ValueLevel",
                "typeText": "forall a b. Ord b => (a -> b) -> Set a -> Set b",
            },
            "markup": "<p>Maps over the values in a set.</p>\n",
            "package": "purescript-ordered-collections",
            "text": "Maps over the values in a set.\n",
            "url": "https://pursuit.purescript.org/packages/purescript-ordered-collections/3.2.0/docs/Data.Set#v:map",
            "version": "3.2.0",
        },
        {
            "info": {
                "module": "Data.Map.Internal",
                "title": "Map",
                "type": "declaration",
                "typeOrValue": "TypeLevel",
                "typeText": None,
            },
            "markup": "<p>Map type</p>\n",
            "package": "purescript-ordered-collections",
            "text": "Map type\n",
            "url": "https://pursuit.purescript.org/packages/purescript-ordered-collections/3.2.0/docs/Data.Map.Internal#t:Map",
            "version": "3.2.0",
        },
    ]
    httpx_mock.add_response(json=api_response)

    # Search with limit=2
    search_results = await search("map", limit=2)

    # Format the results
    formatted = format(search_results)

    # Expected formatted output (only first 2 results)
    expected: FormatOutput = {
        "results": [
            {
                "package": "purescript-prelude",
                "version": "6.0.2",
                "docs": "Map function\n",
                "type": "declaration",
                "url": "https://pursuit.purescript.org/packages/purescript-prelude/6.0.2/docs/Data.Functor#v:map",
            },
            {
                "package": "purescript-ordered-collections",
                "version": "3.2.0",
                "docs": "Maps over the values in a set.\n",
                "type": "declaration",
                "url": "https://pursuit.purescript.org/packages/purescript-ordered-collections/3.2.0/docs/Data.Set#v:map",
            },
        ],
        "count": 2,
    }

    assert formatted == expected
