# Model Context Protocol: Architecture & Tool Design Patterns

This guide defines the architectural blueprints and tool surface design patterns for building robust, scalable MCP servers for LLM agents.

---

## 1. Tool Surface Design Patterns

Choosing the right tool interface pattern is critical to avoid context exhaustion and cognitive overload on the agent.

### Pattern A: Discrete 1:1 Tools (< 15 Actions)
- **When to use**: Small APIs, local system utilities, dedicated single-purpose databases.
- **Characteristics**: Each action is a distinct tool (e.g. `db_query`, `db_insert`, `db_list_tables`).
- **Guidelines**: Keep schemas explicit. Use Pydantic or Zod to enforce strict types and default values.

### Pattern B: Search + Execute (> 15 Actions / Large APIs)
- **When to use**: Wrapping large REST APIs (GitHub, Jira, AWS, Slack) with dozens of endpoints.
- **Why**: Exposing 50+ tools directly floods the agent's context window with tool schemas, degrading reasoning accuracy.
- **Architecture**:
  1. `api_search_endpoints(query: str)` ──► Returns relevant endpoint signatures.
  2. `api_execute_endpoint(endpoint: str, params: dict)` ──► Executes the chosen endpoint.

### Pattern C: State Machine / Relational Trees (e.g., Campaigns MCP)
- **When to use**: Complex relational databases or multi-step operational workflows.
- **Characteristics**: Read operations provide hierarchical context (e.g., tasks with subtasks and active strikes). Writes enforce atomic validation.

---

## 2. Server Frameworks: Python (FastMCP) vs. TypeScript

| Feature | Python FastMCP (`fastmcp` / `mcp`) | TypeScript SDK (`@modelcontextprotocol/sdk`) |
| :--- | :--- | :--- |
| **Best For** | Data science, SQLite/Postgres DBs, OS automation, rapid prototyping. | Web APIs, Node.js tooling, streaming server-sent events (SSE). |
| **Typing** | Python type hints & Pydantic models. | TypeScript types & Zod schemas. |
| **Transport** | `stdio` (local subprocess) or `sse` (HTTP). | `stdio` or `sse` (Express/Hono). |

---

## 3. Error Handling & Defense In Depth

1. **Structured Errors Over Crashes**:
   Never let an unhandled exception crash the `stdio` JSON-RPC process. Return structured error strings in the tool response content:
   ```python
   # Correct:
   return {"status": "error", "message": f"Table '{table_name}' not found."}
   ```
2. **Context Window Protection**:
   Cap large payloads. If an SQL query or API response returns >100KB, truncate or provide pagination parameters (`limit`, `offset`).
3. **Idempotency & Safety**:
   Flag destructive actions (DROP, DELETE, OVERWRITE) clearly in the tool description.
