---
name: mcp-foundry
description: >-
  Master Model Context Protocol (MCP) server architect, scaffolder, and integration governor.
  Use whenever designing, building, debugging, or registering custom MCP servers for Antigravity,
  wrapping external REST/GraphQL APIs, creating FastMCP Python or TypeScript stdio tools,
  or configuring mcp_config.json, even if the user just asks to "build an MCP" or "expose a tool."
---

# 🔌 MCP Foundry: Model Context Protocol Engineering Suite

Use this skill when architecting, building, debugging, or connecting custom MCP servers into Antigravity or AI agent ecosystems.

---

## 🏛️ Core Principles & Architecture

MCP servers act as bridgeheads between language models and local/remote execution surfaces.
To avoid context bloat and brittle schemas, adhere strictly to our design standards:

1. **Tool Hierarchy & Surface Patterns**:
   - Discrete Tools (<15 actions) vs. Search+Execute (>15 actions).
   - See detailed patterns in [Architecture Patterns](./references/architecture_patterns.md).
2. **Antigravity Registration & Lifecycle**:
   - Configuration in `~/.gemini/config/mcp_config.json` or `.agents/mcp_config.json`.
   - Lazy (`call_mcp_tool`) vs Eager loading mechanics.
   - See integration runbook in [AGY Integration Guide](./references/agy_integration.md).

---

## 🔄 End-to-End MCP Development Workflow

### Step 1: Interface Discovery & Surface Selection
Clarify the target system:
- **Local Data / System Utility** $\rightarrow$ Python FastMCP with `stdio`.
- **High-throughput Web / SSE Service** $\rightarrow$ TypeScript `@modelcontextprotocol/sdk` with SSE/stdio.
- **Surface Sizing**: If API has dozens of endpoints, design a Search+Execute interface rather than dumping 50 tools into context.

### Step 2: Automated Scaffolding
Generate a production-ready template using the bundled foundry scaffolder:

```bash
# Python FastMCP:
python ~/.gemini/antigravity-cli/skills/mcp-foundry/scripts/scaffold_mcp.py <destination_dir> <server_name> python

# TypeScript:
python ~/.gemini/antigravity-cli/skills/mcp-foundry/scripts/scaffold_mcp.py <destination_dir> <server_name> typescript
```

### Step 3: Implement & Secure Tool Logic
- Enforce strict typing with Pydantic (Python) or Zod (TypeScript).
- Trap all exceptions; return structured JSON payloads (`{"status": "error", "message": "..."}`) instead of crashing the `stdio` process.
- Truncate large payloads (>100KB) to protect agent context.

### Step 4: Antigravity Registration & Verification
1. Add entry to `~/.gemini/config/mcp_config.json`.
2. Verify local execution without silent crashes.
3. Test tool discovery and lazy-loading schemas.
