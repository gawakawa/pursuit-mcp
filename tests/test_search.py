#!/usr/bin/env python
"""Simple test script for search_pursuit function."""

import asyncio
import json

from pursuit_mcp.search import search

# 表示する結果の最大件数
MAX_RESULTS = 3

# 検索クエリとその説明
QUERIES = [
    ("関数名検索", "map"),
    ("型シグネチャ検索", "(a -> b) -> f a -> f b"),
    ("モジュール検索", "Data.Array"),
    ("パッケージ検索", "prelude"),
]


async def main():
    for description, query in QUERIES:
        print(f"\n{'=' * 60}")
        print(f"{description}: {query}")
        print("=" * 60)
        results = await search(query)
        limited_results = results[:MAX_RESULTS]
        print(json.dumps(limited_results, indent=2, ensure_ascii=False))
        if len(results) > MAX_RESULTS:
            print(f"\n... and {len(results) - MAX_RESULTS} more results")


if __name__ == "__main__":
    asyncio.run(main())
