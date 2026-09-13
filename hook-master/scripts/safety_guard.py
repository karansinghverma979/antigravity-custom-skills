#!/usr/bin/env python3
"""
PreToolUse Safety Gate Hook Handler
Intercepts dangerous, unparameterized, or destructive operations before execution.
"""

import sys
import json
import re

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DESTRUCTIVE_PATTERNS = [
    (r"DROP\s+TABLE", "DROP TABLE statement detected in SQL execution"),
    (r"TRUNCATE\s+TABLE", "TRUNCATE TABLE statement detected in SQL execution"),
    (r"rm\s+-rf\s+[\/\\]", "Root recursive deletion detected"),
    (r"Remove-Item\s+.*-Recurse.*[\/\\]$", "Broad recursive filesystem deletion"),
    (r"format\s+[a-zA-Z]:", "Disk format command detected"),
]

def main():
    try:
        raw_input = sys.stdin.read()
        input_data = json.loads(raw_input) if raw_input else {}
    except Exception:
        input_data = {}

    tool_call = input_data.get("toolCall", {})
    tool_name = tool_call.get("name", "")
    args = tool_call.get("args", {})

    cmd_line = args.get("CommandLine", "") or args.get("query", "") or str(args)

    for pattern, desc in DESTRUCTIVE_PATTERNS:
        if re.search(pattern, cmd_line, re.IGNORECASE):
            response = {
                "decision": "ask",
                "reason": f"[SAFETY GATE] Dangerous operation intercepted: {desc}."
            }
            print(json.dumps(response))
            return

    # Default: allow
    response = {
        "decision": "allow"
    }
    print(json.dumps(response))

if __name__ == "__main__":
    main()
