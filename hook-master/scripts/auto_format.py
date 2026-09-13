#!/usr/bin/env python3
"""
PostToolUse Auto-Formatter Hook Handler
Removes trailing whitespace and ensures clean UTF-8 formatting on modified files.
"""

import sys
import json
import os
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def format_file(file_path: Path):
    if not file_path.is_file():
        return
    if file_path.suffix not in [".py", ".md", ".json", ".ts", ".js", ".ps1"]:
        return

    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
        lines = [line.rstrip() for line in content.splitlines()]
        new_content = "\n".join(lines) + "\n"
        if new_content != content:
            file_path.write_text(new_content, encoding="utf-8")
    except Exception:
        pass

def main():
    try:
        raw_input = sys.stdin.read()
        input_data = json.loads(raw_input) if raw_input else {}
    except Exception:
        input_data = {}

    tool_call = input_data.get("toolCall", {})
    args = tool_call.get("args", {})
    target_file = args.get("TargetFile") or args.get("path") or args.get("file_path")

    if target_file:
        format_file(Path(target_file).resolve())

    # Return valid PostToolUse payload
    print(json.dumps({}))

if __name__ == "__main__":
    main()
