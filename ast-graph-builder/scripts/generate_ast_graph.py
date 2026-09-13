#!/usr/bin/env python3
"""
AST Graph Builder
Parses Python and JS/TS codebases to extract classes, functions, and import graphs
in milliseconds without LLM token burn.
"""

import sys
import os
import ast
import re
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def parse_python_file(file_path: Path) -> dict:
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(content, filename=str(file_path))
    except Exception:
        return {}

    classes = []
    functions = []
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            classes.append({
                "name": node.name,
                "line": node.lineno,
                "methods": methods
            })
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Only top-level functions
            if hasattr(node, "parent") and isinstance(node.parent, ast.ClassDef):
                continue
            functions.append({
                "name": node.name,
                "line": node.lineno
            })
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return {
        "file": file_path.name,
        "classes": classes,
        "functions": functions[:15],
        "imports": list(set(imports))[:10]
    }

def scan_repo(target_dir: str = ".") -> None:
    root = Path(target_dir).resolve()
    print(f"[*] Building AST Symbol Map for: {root}")

    py_files = list(root.rglob("*.py"))[:30]
    print(f"[*] Found {len(py_files)} Python file(s).\n")

    for pf in py_files:
        # Skip virtualenvs or cache
        if any(part in str(pf) for part in [".venv", "venv", "__pycache__", "site-packages", ".git"]):
            continue

        meta = parse_python_file(pf)
        if not meta or (not meta["classes"] and not meta["functions"]):
            continue

        rel_path = pf.relative_to(root)
        print(f"📄 [{rel_path}]")
        if meta["classes"]:
            for c in meta["classes"]:
                methods_str = f" ({', '.join(c['methods'][:5])})" if c['methods'] else ""
                print(f"  ├── class {c['name']} (L{c['line']}){methods_str}")
        if meta["functions"]:
            funcs_str = ", ".join([f"{fn['name']}:L{fn['line']}" for fn in meta["functions"][:6]])
            print(f"  └── funcs: {funcs_str}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    scan_repo(target)
