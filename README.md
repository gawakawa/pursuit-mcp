# Pursuit MCP

MCP server providing [Pursuit](https://pursuit.purescript.org/) integration for PureScript documentation search.

## Features

- Search Pursuit for PureScript functions, types, modules, and packages
- Type signature search support
- Access to comprehensive PureScript package documentation

## Usage

### MCP Client Configuration

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "pursuit": {
      "command": "nix",
      "args": ["run", "github:gawakawa/pursuit-mcp", "--"]
    }
  }
}
```

## Available Tools

### `search_pursuit`

Search Pursuit for PureScript functions, types, and documentation.

**Parameters:**
- `query` (string): Search query (function name, type signature, or keyword)
- `limit` (integer, optional): Maximum number of results to return (default: 10)

**Examples:**
- Function name search: `map`
- Type signature search: `(a -> b) -> f a -> f b`
- Module search: `Data.Array`
- Package search: `prelude`

**Response Format:**
Each result includes:
- `package`: Package name (e.g., "purescript-prelude")
- `version`: Package version
- `info`: Result type and metadata
  - For declarations: includes module, title, type signature
  - For packages: includes deprecation status
  - For modules: includes module name
- `text`: Plain text documentation
- `url`: Direct link to the documentation
- `markup`: HTML-formatted documentation (optional)

## License

MIT
