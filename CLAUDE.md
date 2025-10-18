# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

MCP server providing Pursuit integration for PureScript documentation search. Built with FastMCP framework using Python 3.12+ and Nix flake for development environment.

## Project Structure

```
src/pursuit_mcp/
  ├── server.py         # FastMCP server with search_pursuit tool
  ├── search.py         # Pursuit API client (async httpx)
  ├── format.py         # Result formatting
  └── __init__.py
tests/
  └── test_search.py    # Test script for search functionality
```

## Development Environment

Uses direnv for automatic environment setup. Provides Python 3.12, ruff, and uv.

**Install dependencies**:
```bash
uv sync
```

**Add new dependency**:
```bash
uv add <package>
```

**IMPORTANT**: Always use `uv add` to add dependencies. NEVER manually edit pyproject.toml for dependency management.

## When to Use NixOS MCP

NixOS MCP provides real-time access to NixOS ecosystem data (130K+ packages, 22K+ options). Use these tools when:

**Package Management**:
- `nixos_search(query, "packages")` - Search for packages to add to `flake.nix` or development environment
- `nixos_info(name, "package")` - Get detailed package information (version, description, homepage, license)
- `nixos_channels()` - List available channels (stable, unstable, specific versions)

**Version History** (via NixHub.io):
- `nixhub_package_versions(package)` - Get version history with nixpkgs commit hashes for reproducible builds
- `nixhub_find_version(package, version)` - Find specific package versions (e.g., "ruby", "2.6.7")

**Configuration Options**:
- `nixos_search(query, "options")` - Search NixOS configuration options for flake setup
- `home_manager_search(query)` - Search Home Manager options (4K+ user config settings)
- `darwin_search(query)` - Search nix-darwin options (1K+ macOS-specific settings)

**Flake Discovery**:
- `nixos_flakes_search(query)` - Search community flakes for additional functionality

All tools return plain text output with current data from search.nixos.org APIs.

## Common Commands

**Run the server**:
```bash
uv run pursuit-mcp
```

**Run test script**:
```bash
uv run tests/test_search.py
```

**Format code**:
```bash
ruff format .
```

**Lint code**:
```bash
ruff check .
```

**Fix linting issues**:
```bash
ruff check --fix .
```

**Format check (CI equivalent)**:
```bash
ruff format --check --diff
```

## Code Quality

- CI enforces Ruff formatting and linting on all pushes/PRs
- Format code before committing
- Python 3.12+ required

## Key Dependencies

- **fastmcp**: FastMCP framework for building MCP servers
- **httpx**: Async HTTP client for Pursuit API requests
- **mcp**: Model Context Protocol SDK

## MCP Tools

**search_pursuit**: Search Pursuit for PureScript functions, types, and documentation
- Takes a query string (function name, type signature, or keyword)
- Takes an optional limit parameter (default: 10)
- Returns formatted search results from Pursuit API as JSON

**Response Format**:
Each result includes:
- `package`: Package name (e.g., "purescript-prelude")
- `version`: Package version
- `info`: Result type and metadata
  - `type`: "declaration", "module", or "package"
  - For declarations: includes module, title, type signature
  - For packages: includes deprecation status
  - For modules: includes module name
- `text`: Plain text documentation
- `url`: Direct link to the documentation
- `markup`: HTML-formatted documentation

## References

**Pursuit**:
- https://pursuit.purescript.org/ - Official Pursuit search service for PureScript documentation
- https://github.com/purescript/pursuit - Pursuit source code and documentation. Refer when understanding API behavior or implementing features
- https://github.com/purescript/pursuit/blob/master/src/Handler/Search.hs - Search handler implementation showing API structure

**MCP**:
- https://modelcontextprotocol.io/docs/develop/build-server#python - Official Python MCP server guide. Reference when implementing server structure, tools, or resources
- https://github.com/jlowin/fastmcp - FastMCP library documentation. Use when working with FastMCP-specific features or patterns
