"""Test suite for Pursuit search functionality with expected data."""

import pytest
from pytest_httpx import HTTPXMock

from pursuit_mcp.search import search

# Expected data based on actual Pursuit API responses
# Declaration type: info has module, title, type, typeOrValue, typeText
# Module type: info has module, type
# Package type: info has deprecated, type
expected_map_search = [
    {
        "info": {
            "module": "Data.Functor",
            "title": "map",
            "type": "declaration",
            "typeOrValue": "ValueLevel",
            "typeText": "forall f a b. Functor f => (a -> b) -> f a -> f b",
        },
        "markup": "\n",
        "package": "purescript-prelude",
        "text": "",
        "url": "https://pursuit.purescript.org/packages/purescript-prelude/6.0.2/docs/Data.Functor#v:map",
        "version": "6.0.2",
    },
    {
        "info": {
            "module": "Data.Map.Internal",
            "title": "Map",
            "type": "declaration",
            "typeOrValue": "TypeLevel",
            "typeText": None,
        },
        "markup": "<p><code>Map k v</code> represents maps from keys of type <code>k</code> to values of type <code>v</code>.</p>\n",
        "package": "purescript-ordered-collections",
        "text": "`Map k v` represents maps from keys of type `k` to values of type `v`.\n",
        "url": "https://pursuit.purescript.org/packages/purescript-ordered-collections/3.2.0/docs/Data.Map.Internal#t:Map",
        "version": "3.2.0",
    },
    {
        "info": {
            "module": "Data.Set",
            "title": "map",
            "type": "declaration",
            "typeOrValue": "ValueLevel",
            "typeText": "forall a b. Ord b => (a -> b) -> Set a -> Set b",
        },
        "markup": "<p>Maps over the values in a set.</p>\n<p>This operation is not structure-preserving for sets, so is not a valid\n<code>Functor</code>. An example case: mapping <code>const x</code> over a set with <code>n &gt; 0</code>\nelements will result in a set with one element.</p>\n",
        "package": "purescript-ordered-collections",
        "text": "Maps over the values in a set.\n\nThis operation is not structure-preserving for sets, so is not a valid\n`Functor`. An example case: mapping `const x` over a set with `n > 0`\nelements will result in a set with one element.\n",
        "url": "https://pursuit.purescript.org/packages/purescript-ordered-collections/3.2.0/docs/Data.Set#v:map",
        "version": "3.2.0",
    },
]

expected_type_signature_search = [
    {
        "info": {
            "module": "Control.Applicative",
            "title": "liftA1",
            "type": "declaration",
            "typeOrValue": "ValueLevel",
            "typeText": "forall f a b. Applicative f => (a -> b) -> f a -> f b",
        },
        "markup": '<p><code>liftA1</code> provides a default implementation of <code>(&lt;$&gt;)</code> for any\n<code>Applicative</code> functor, without using <code>(&lt;$&gt;)</code> as provided\nby the <code>Functor</code>-<code>Applicative</code> superclass\nrelationship.</p>\n<p><code>liftA1</code> can therefore be used to write <code>Functor</code> instances\nas follows:</p>\n<pre class="purescript"><code>instance functorF :: Functor F where\n  map = liftA1\n</code></pre>\n',
        "package": "purescript-prelude",
        "text": "`liftA1` provides a default implementation of `(<$>)` for any\n[`Applicative`](#applicative) functor, without using `(<$>)` as provided\nby the [`Functor`](#functor)-[`Applicative`](#applicative) superclass\nrelationship.\n\n`liftA1` can therefore be used to write [`Functor`](#functor) instances\nas follows:\n\n```purescript\ninstance functorF :: Functor F where\n  map = liftA1\n```\n",
        "url": "https://pursuit.purescript.org/packages/purescript-prelude/6.0.2/docs/Control.Applicative#v:liftA1",
        "version": "6.0.2",
    },
    {
        "info": {
            "module": "Control.Monad",
            "title": "liftM1",
            "type": "declaration",
            "typeOrValue": "ValueLevel",
            "typeText": "forall m a b. Monad m => (a -> b) -> m a -> m b",
        },
        "markup": '<p><code>liftM1</code> provides a default implementation of <code>(&lt;$&gt;)</code> for any\n<code>Monad</code>, without using <code>(&lt;$&gt;)</code> as provided by the\n<code>Functor</code>-<code>Monad</code> superclass relationship.</p>\n<p><code>liftM1</code> can therefore be used to write <code>Functor</code> instances\nas follows:</p>\n<pre class="purescript"><code>instance functorF :: Functor F where\n  map = liftM1\n</code></pre>\n',
        "package": "purescript-prelude",
        "text": "`liftM1` provides a default implementation of `(<$>)` for any\n[`Monad`](#monad), without using `(<$>)` as provided by the\n[`Functor`](#functor)-[`Monad`](#monad) superclass relationship.\n\n`liftM1` can therefore be used to write [`Functor`](#functor) instances\nas follows:\n\n```purescript\ninstance functorF :: Functor F where\n  map = liftM1\n```\n",
        "url": "https://pursuit.purescript.org/packages/purescript-prelude/6.0.2/docs/Control.Monad#v:liftM1",
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
        "markup": "\n",
        "package": "purescript-prelude",
        "text": "",
        "url": "https://pursuit.purescript.org/packages/purescript-prelude/6.0.2/docs/Data.Functor#v:map",
        "version": "6.0.2",
    },
]

expected_module_search = [
    {
        "info": {"module": "Data.Array", "type": "module"},
        "markup": "<p>Helper functions for working with immutable Javascript arrays.</p>\n<p><em>Note</em>: Depending on your use-case, you may prefer to use <code>Data.List</code> or\n<code>Data.Sequence</code> instead, which might give better performance for certain\nuse cases. This module is useful when integrating with JavaScript libraries\nwhich use arrays, but immutable arrays are not a practical data structure\nfor many use cases due to their poor asymptotics.</p>\n<p>In addition to the functions in this module, Arrays have a number of\nuseful instances:</p>\n<ul>\n<li><code>Functor</code>, which provides <code>map :: forall a b. (a -&gt; b) -&gt; Array a -&gt;\nArray b</code></li>\n<li><code>Apply</code>, which provides <code>(&lt;*&gt;) :: forall a b. Array (a -&gt; b) -&gt; Array a\n-&gt; Array b</code>. This function works a bit like a Cartesian product; the\nresult array is constructed by applying each function in the first\narray to each value in the second, so that the result array ends up with\na length equal to the product of the two arguments&#39; lengths.</li>\n<li><code>Bind</code>, which provides <code>(&gt;&gt;=) :: forall a b. (a -&gt; Array b) -&gt; Array a\n-&gt; Array b</code> (this is the same as <code>concatMap</code>).</li>\n<li><code>Semigroup</code>, which provides <code>(&lt;&gt;) :: forall a. Array a -&gt; Array a -&gt;\nArray a</code>, for concatenating arrays.</li>\n<li><code>Foldable</code>, which provides a slew of functions for <em>folding</em> (also known\nas <em>reducing</em>) arrays down to one value. For example,\n<code>Data.Foldable.or</code> tests whether an array of <code>Boolean</code> values contains\nat least one <code>true</code> value.</li>\n<li><code>Traversable</code>, which provides the PureScript version of a for-loop,\nallowing you to STAI.iterate over an array and accumulate effects.</li>\n</ul>\n",
        "package": "purescript-arrays",
        "text": "Helper functions for working with immutable Javascript arrays.\n\n_Note_: Depending on your use-case, you may prefer to use `Data.List` or\n`Data.Sequence` instead, which might give better performance for certain\nuse cases. This module is useful when integrating with JavaScript libraries\nwhich use arrays, but immutable arrays are not a practical data structure\nfor many use cases due to their poor asymptotics.\n\nIn addition to the functions in this module, Arrays have a number of\nuseful instances:\n\n* `Functor`, which provides `map :: forall a b. (a -> b) -> Array a ->\n  Array b`\n* `Apply`, which provides `(<*>) :: forall a b. Array (a -> b) -> Array a\n  -> Array b`. This function works a bit like a Cartesian product; the\n  result array is constructed by applying each function in the first\n  array to each value in the second, so that the result array ends up with\n  a length equal to the product of the two arguments' lengths.\n* `Bind`, which provides `(>>=) :: forall a b. (a -> Array b) -> Array a\n  -> Array b` (this is the same as `concatMap`).\n* `Semigroup`, which provides `(<>) :: forall a. Array a -> Array a ->\n  Array a`, for concatenating arrays.\n* `Foldable`, which provides a slew of functions for *folding* (also known\n  as *reducing*) arrays down to one value. For example,\n  `Data.Foldable.or` tests whether an array of `Boolean` values contains\n  at least one `true` value.\n* `Traversable`, which provides the PureScript version of a for-loop,\n  allowing you to STAI.iterate over an array and accumulate effects.\n\n",
        "url": "https://pursuit.purescript.org/packages/purescript-arrays/7.3.0/docs/Data.Array",
        "version": "7.3.0",
    },
    {
        "info": {"module": "Data.Array.ST", "type": "module"},
        "markup": "<p>Helper functions for working with mutable arrays using the <code>ST</code> effect.</p>\n<p>This module can be used when performance is important and mutation is a local effect.</p>\n",
        "package": "purescript-arrays",
        "text": "Helper functions for working with mutable arrays using the `ST` effect.\n\nThis module can be used when performance is important and mutation is a local effect.\n",
        "url": "https://pursuit.purescript.org/packages/purescript-arrays/7.3.0/docs/Data.Array.ST",
        "version": "7.3.0",
    },
    {
        "info": {"module": "Data.ArrayView", "type": "module"},
        "markup": "\n",
        "package": "purescript-array-views",
        "text": "",
        "url": "https://pursuit.purescript.org/packages/purescript-array-views/0.0.2/docs/Data.ArrayView",
        "version": "0.0.2",
    },
]

expected_package_search = [
    {
        "info": {"deprecated": False, "type": "package"},
        "markup": "<p>The PureScript Prelude</p>\n",
        "package": "purescript-prelude",
        "text": "The PureScript Prelude",
        "url": "https://pursuit.purescript.org/packages/purescript-prelude",
        "version": "6.0.2",
    },
    {
        "info": {"module": "Prelude", "type": "module"},
        "markup": "<p><code>Prelude</code> is a module that re-exports many other foundational modules from the <code>purescript-prelude</code> library\n(e.g. the Monad type class hierarchy, the Monoid type classes, Eq, Ord, etc.).</p>\n<p>Typically, this module will be imported in most other libraries and projects as an open import.</p>\n<pre><code>module MyModule where\n\nimport Prelude -- open import\n\nimport Data.Maybe (Maybe(..)) -- closed import\n</code></pre>\n",
        "package": "purescript-prelude",
        "text": "`Prelude` is a module that re-exports many other foundational modules from the `purescript-prelude` library\n(e.g. the Monad type class hierarchy, the Monoid type classes, Eq, Ord, etc.).\n\nTypically, this module will be imported in most other libraries and projects as an open import.\n\n```\nmodule MyModule where\n\nimport Prelude -- open import\n\nimport Data.Maybe (Maybe(..)) -- closed import\n```\n",
        "url": "https://pursuit.purescript.org/packages/purescript-prelude/6.0.2/docs/Prelude",
        "version": "6.0.2",
    },
    {
        "info": {"module": "Prelude.Unicode", "type": "module"},
        "markup": "\n",
        "package": "purescript-unicode-prelude",
        "text": "",
        "url": "https://pursuit.purescript.org/packages/purescript-unicode-prelude/0.2.4/docs/Prelude.Unicode",
        "version": "0.2.4",
    },
]


@pytest.mark.asyncio
async def test_search_function_name_map(httpx_mock: HTTPXMock):
    """Test searching for 'map' function returns expected results."""
    httpx_mock.add_response(json=expected_map_search)

    results = await search("map", limit=3)
    assert results == expected_map_search


@pytest.mark.asyncio
async def test_search_type_signature(httpx_mock: HTTPXMock):
    """Test searching by type signature returns expected results."""
    httpx_mock.add_response(json=expected_type_signature_search)

    results = await search("(a -> b) -> f a -> f b", limit=3)
    assert results == expected_type_signature_search


@pytest.mark.asyncio
async def test_search_module_data_array(httpx_mock: HTTPXMock):
    """Test searching for 'Data.Array' module returns expected results."""
    httpx_mock.add_response(json=expected_module_search)

    results = await search("Data.Array", limit=3)
    assert results == expected_module_search


@pytest.mark.asyncio
async def test_search_package_prelude(httpx_mock: HTTPXMock):
    """Test searching for 'prelude' package returns expected results."""
    httpx_mock.add_response(json=expected_package_search)

    results = await search("prelude", limit=3)
    assert results == expected_package_search


@pytest.mark.asyncio
async def test_search_limit_parameter(httpx_mock: HTTPXMock):
    """Test that limit parameter correctly limits results."""
    # Mock API returns 12 results
    full_results = expected_map_search * 4  # 12 results
    httpx_mock.add_response(json=full_results)

    limit = 3
    results = await search("map", limit=limit)

    assert len(results) == limit
    assert results == full_results[:limit]


@pytest.mark.asyncio
async def test_search_default_limit(httpx_mock: HTTPXMock):
    """Test default limit of 10 results."""
    full_results = expected_map_search * 10  # 30 results
    httpx_mock.add_response(json=full_results)

    results = await search("map")  # default limit=10

    assert len(results) == 10
    assert results == full_results[:10]
