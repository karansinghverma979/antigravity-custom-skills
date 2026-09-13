#!/usr/bin/env python3
"""
MCP Foundry Server Scaffolder
Generates production-ready FastMCP (Python) or TypeScript MCP server boilerplates
with UTF-8 safe logging, schema definitions, and Windows-ready configs.
"""

import sys
import os
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

PYTHON_FASTMCP_TEMPLATE = '''#!/usr/bin/env python3
"""
{server_name} - MCP Server
Built with FastMCP for Google Antigravity & AI Agent ecosystems.
"""

import os
import sys
from mcp.server.fastmcp import FastMCP

# Ensure UTF-8 output streams
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

mcp = FastMCP("{server_name}")

@mcp.tool()
def health_check() -> dict:
    """Verify server health and operational status."""
    return {{
        "status": "healthy",
        "server": "{server_name}",
        "version": "1.0.0"
    }}

@mcp.tool()
def execute_operation(query: str, limit: int = 10) -> dict:
    """
    Execute sample query operation.
    
    Args:
        query: The search query or operation instruction
        limit: Max results to return (default: 10)
    """
    return {{
        "status": "success",
        "query": query,
        "results": [f"Result item for '{{query}}' (#{{i}})" for i in range(1, limit + 1)]
    }}

if __name__ == "__main__":
    mcp.run(transport="stdio")
'''

TYPESCRIPT_TEMPLATE = '''import {{ Server }} from "@modelcontextprotocol/sdk/server/index.js";
import {{ StdioServerTransport }} from "@modelcontextprotocol/sdk/server/stdio.js";
import {{
  CallToolRequestSchema,
  ListToolsRequestSchema,
}} from "@modelcontextprotocol/sdk/types.js";
import {{ z }} from "zod";

const server = new Server(
  {{
    name: "{server_name}",
    version: "1.0.0",
  }},
  {{
    capabilities: {{
      tools: {{}},
    }},
  }}
);

// Define available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {{
  return {{
    tools: [
      {{
        name: "health_check",
        description: "Verify server health and status",
        inputSchema: {{
          type: "object",
          properties: {{}},
        }},
      }},
    ],
  }};
}});

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {{
  if (request.params.name === "health_check") {{
    return {{
      content: [
        {{
          type: "text",
          text: JSON.stringify({{ status: "healthy", server: "{server_name}" }}),
        }},
      ],
    }};
  }}
  throw new Error(`Unknown tool: ${{request.params.name}}`);
}});

async function run() {{
  const transport = new StdioServerTransport();
  await server.connect(transport);
}}

run().catch(console.error);
'''

def scaffold_server(target_dir: str, server_name: str, lang: str = "python") -> bool:
    out_dir = Path(target_dir).resolve() / server_name
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Scaffolding MCP Server: '{server_name}' ({lang}) at {out_dir}")

    if lang.lower() == "python":
        server_file = out_dir / "server.py"
        server_file.write_text(PYTHON_FASTMCP_TEMPLATE.format(server_name=server_name), encoding="utf-8")
        
        req_file = out_dir / "requirements.txt"
        req_file.write_text("mcp>=1.0.0\npydantic>=2.0.0\n", encoding="utf-8")
        
        readme_file = out_dir / "README.md"
        readme_content = f"""# {server_name} MCP Server

## Run locally:
```bash
python server.py
```

## Register in ~/.gemini/config/mcp_config.json:
```json
{{
  "mcpServers": {{
    "{server_name}": {{
      "command": "python",
      "args": ["{str(server_file).replace('\\\\', '/')}"]
    }}
  }}
}}
```
"""
        readme_file.write_text(readme_content, encoding="utf-8")
    else:
        src_dir = out_dir / "src"
        src_dir.mkdir(parents=True, exist_ok=True)
        (src_dir / "index.ts").write_text(TYPESCRIPT_TEMPLATE.format(server_name=server_name), encoding="utf-8")
        
        pkg_json = out_dir / "package.json"
        pkg_content = f"""{{
  "name": "{server_name}",
  "version": "1.0.0",
  "type": "module",
  "scripts": {{
    "build": "tsc",
    "start": "node dist/index.js"
  }},
  "dependencies": {{
    "@modelcontextprotocol/sdk": "^1.0.0",
    "zod": "^3.22.0"
  }},
  "devDependencies": {{
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0"
  }}
}}
"""
        pkg_json.write_text(pkg_content, encoding="utf-8")

    print(f"[OK] Server '{server_name}' successfully scaffolded.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scaffold_mcp.py <target_directory> <server_name> [python|typescript]")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    name = sys.argv[2]
    lang = sys.argv[3] if len(sys.argv) > 3 else "python"
    scaffold_server(target_dir, name, lang)
