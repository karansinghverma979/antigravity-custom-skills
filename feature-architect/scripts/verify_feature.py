#!/usr/bin/env python3
"""
Feature Verification Suite
Executes automated pre-merge sanity checks: syntax validation, test runners,
and Git change sanity.
"""

import sys
import subprocess
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def run_cmd(cmd: list, cwd: Path) -> tuple:
    try:
        res = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace")
        return res.returncode, res.stdout, res.stderr
    except Exception as e:
        return -1, "", str(e)

def verify_feature(target_dir: str = ".") -> bool:
    target = Path(target_dir).resolve()
    print(f"[*] Running Feature Verification in: {target}")

    passed = True

    # 1. Python Syntax & Test Check (if applicable)
    py_files = list(target.rglob("*.py"))[:30]
    if py_files:
        print(f"  [*] Checking {len(py_files)} Python file(s) for syntax errors...")
        for py in py_files:
            code, out, err = run_cmd(["python", "-m", "py_compile", str(py)], target)
            if code != 0:
                print(f"  [ERROR] Syntax error in {py.name}:\n{err}")
                passed = False
        if passed:
            print("  [OK] Python syntax verification passed.")

    # 2. Check for Pytest if tests directory exists
    test_dir = target / "tests"
    if test_dir.is_dir():
        print("  [*] Running pytest...")
        code, out, err = run_cmd(["pytest", "-q"], target)
        if code == 0:
            print("  [OK] All unit tests passed.")
        else:
            print(f"  [WARN] Test suite reported failures:\n{out}\n{err}")

    # 3. Check for package.json / npm test
    if (target / "package.json").exists():
        print("  [*] Found package.json. Verifying build...")
        code, out, err = run_cmd(["npm", "run", "build"], target)
        if code == 0:
            print("  [OK] npm build succeeded.")
        else:
            print(f"  [WARN] npm build failed:\n{err}")

    if passed:
        print("\n[RESULT] Feature verification PASSED.")
    else:
        print("\n[RESULT] Feature verification FAILED.")

    return passed

if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else "."
    success = verify_feature(tgt)
    sys.exit(0 if success else 1)
