#!/usr/bin/env python3
"""
Autonomous Loop Runner
Executes a test/build command in a closed loop, reporting structured diagnostics
to enable automated self-healing without infinite execution.
"""

import sys
import subprocess
import re
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def run_step(cmd: str, cwd: str = ".") -> dict:
    print(f"[*] Executing target command: '{cmd}' in {cwd}")
    try:
        proc = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        return {
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "success": proc.returncode == 0
        }
    except Exception as e:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": str(e),
            "success": False
        }

def parse_stack_trace(stderr_text: str, stdout_text: str) -> list:
    combined = stderr_text + "\n" + stdout_text
    # Catch Python / JS / General file:line traces
    file_line_matches = re.findall(r'File "([^"]+)", line (\d+)', combined)
    if not file_line_matches:
        file_line_matches = re.findall(r'([a-zA-Z0-9_\-\/\\]+\.(?:py|js|ts|jsx|tsx)):(\d+)', combined)
    return list(set(file_line_matches))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_loop.py \"<command>\" [cwd]")
        sys.exit(1)

    command = sys.argv[1]
    work_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    result = run_step(command, work_dir)
    if result["success"]:
        print("\n[RESULT] Command PASSED successfully (Exit Code 0).")
        sys.exit(0)
    else:
        print(f"\n[ALERT] Command FAILED (Exit Code {result['exit_code']}).")
        locations = parse_stack_trace(result["stderr"], result["stdout"])
        if locations:
            print("[*] Detected failure locations:")
            for f, l in locations:
                print(f"    - {f}:{l}")
        print("\n--- Error Output ---")
        err_snippet = result["stderr"] or result["stdout"]
        print(err_snippet[-1500:] if len(err_snippet) > 1500 else err_snippet)
        sys.exit(result["exit_code"])
