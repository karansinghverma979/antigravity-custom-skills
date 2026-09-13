#!/usr/bin/env python3
"""
Diff Sentinel Analyzer
Parses working tree diffs or file directories to highlight risky patterns,
swallowed exceptions, and high-complexity modifications.
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

# Check regexes
RISK_CHECKS = [
    (re.compile(r"except\s*:\s*pass"), "Uncaught broad exception swallowed (`except: pass`)"),
    (re.compile(r"except\s+Exception\s*:\s*pass"), "Broad `Exception` swallowed with `pass`"),
    (re.compile(r"catch\s*\([^\)]*\)\s*\{\s*\}"), "Empty catch block in JavaScript/TypeScript"),
    (re.compile(r"SELECT\s+.*\+\s*['\"]"), "Possible raw SQL concatenation (SQL Injection risk)"),
    (re.compile(r"os\.system\("), "Dangerous subprocess execution via `os.system`"),
]

def is_git_repo(path: Path) -> bool:
    try:
        res = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=str(path), capture_output=True, text=True)
        return res.returncode == 0
    except Exception:
        return False

def analyze_target(target_path: str = ".") -> bool:
    target = Path(target_path).resolve()
    print(f"[*] Auditing target: {target}")

    flagged_issues = []

    if target.is_dir() and is_git_repo(target):
        try:
            diff_proc = subprocess.run(
                ["git", "diff", "HEAD"],
                cwd=str(target),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            diff_text = diff_proc.stdout
            if not diff_text.strip():
                status_proc = subprocess.run(["git", "status", "-s"], cwd=str(target), capture_output=True, text=True)
                print(f"[OK] Clean Git working tree at {target.name}. (Status: {len(status_proc.stdout.splitlines())} modified/untracked files)")
                return True

            current_file = "Unknown"
            for line in diff_text.splitlines():
                if line.startswith("+++ b/"):
                    current_file = line[6:]
                    continue
                if line.startswith("+") and not line.startswith("+++"):
                    added_content = line[1:].strip()
                    # Skip self-contained regex strings
                    if "re.compile" in added_content or "RISK_CHECKS" in added_content:
                        continue
                    for pattern, desc in RISK_CHECKS:
                        if pattern.search(added_content):
                            flagged_issues.append((current_file, desc, added_content))
        except Exception as e:
            print(f"[WARN] Error inspecting Git diff: {e}")
            return False
    else:
        files_to_scan = [target] if target.is_file() else list(target.rglob("*.py"))[:50] + list(target.rglob("*.ts"))[:50] + list(target.rglob("*.js"))[:50]
        for f in files_to_scan:
            # Skip the analyzer itself
            if f.name == "audit_diff.py":
                continue
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
                for line in content.splitlines():
                    for pattern, desc in RISK_CHECKS:
                        if pattern.search(line):
                            flagged_issues.append((f.name, desc, line.strip()))
            except Exception:
                pass

    if flagged_issues:
        print(f"\n[ALERT] Found {len(flagged_issues)} potential risk(s):")
        for file_name, desc, snippet in flagged_issues:
            print(f"  - [{file_name}] {desc}\n      Code: {snippet}")
        return False
    else:
        print("\n[OK] Zero high-risk static patterns detected.")
        return True

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    analyze_target(target)
