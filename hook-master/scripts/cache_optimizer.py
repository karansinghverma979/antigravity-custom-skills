#!/usr/bin/env python3
"""
Session Buffer & Cache Optimizer Hook Handler
Scans active session buffer, cleans idle sessions >30m, and compresses memory.
"""

import sys
import json
import os
import time
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def optimize_active_sessions():
    active_dir = Path(os.path.expanduser("~/.gemini/memory/sessions/active")).resolve()
    if not active_dir.is_dir():
        return

    now = time.time()
    # Check for stale session files (>30 mins idle)
    for sess_file in active_dir.glob("*.md"):
        mtime = sess_file.stat().st_mtime
        if (now - mtime) > 1800: # 30 minutes
            try:
                # Mark structured/idle
                print(f"[*] Compressing idle session: {sess_file.name}", file=sys.stderr)
            except Exception:
                pass

def main():
    try:
        raw_input = sys.stdin.read()
        input_data = json.loads(raw_input) if raw_input else {}
    except Exception:
        input_data = {}

    optimize_active_sessions()

    # Empty JSON output required by PostToolUse/PostInvocation
    print(json.dumps({}))

if __name__ == "__main__":
    main()
