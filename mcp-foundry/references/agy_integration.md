# Antigravity MCP Server Integration & Configuration

This guide covers registering, configuring, and optimizing Model Context Protocol (MCP) servers within the Google Antigravity (AGY) runtime on Windows.

---

## 1. Registration Configuration: `mcp_config.json`

Antigravity loads MCP servers defined in `~/.gemini/config/mcp_config.json` (global) or `.agents/mcp_config.json` (workspace-specific).

### Standard Configuration Structure:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": [
        "C:\\path\\to\\my_server\\server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "API_KEY": "secret-token"
      }
    },
    "my-node-server": {
      "command": "node",
      "args": [
        "C:\\path\\to\\my_server\\build\\index.js"
      ]
    }
  }
}
```

---

## 2. Tool Loading: Eager vs. Lazy Loading

Antigravity supports two tool mounting modes to balance token efficiency and latency:

### A. Lazy Loaded Tools (`call_mcp_tool`)
- **Default for most MCP servers**.
- The schemas are written as JSON files in `~/.gemini/antigravity-cli/mcp/<serverName>/<toolName>.json`.
- The system prompt only contains the tool name list; when the agent needs a tool, it reads the schema on demand and invokes `call_mcp_tool`.
- **Advantage**: Saves massive system prompt tokens when servers have dozens of tools.

### B. Eagerly Loaded Tools (`mcp_<serverName>_<toolName>`)
- High-frequency tools registered directly as native tool definitions in the agent's core context.
- **Advantage**: Zero extra round-trips for schema reading.

---

## 3. Windows Specific Execution Invariants

1. **Path Formatting**: In `mcp_config.json`, always use double-escaped backslashes (`C:\\Users\\...`) or standard forward slashes (`C:/Users/...`).
2. **Environment Variables**:
   - For Python MCP servers, always set `"PYTHONUNBUFFERED": "1"` so JSON-RPC stdout frames are flushed immediately to AGY.
   - Ensure `PYTHONUTF8: "1"` is set if reading non-ASCII file paths.
3. **Executable Paths**: On Windows, specify full paths if commands rely on virtual environments (`.venv/Scripts/python.exe`).
