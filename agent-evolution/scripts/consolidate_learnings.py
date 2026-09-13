#!/usr/bin/env python3
"""
Learnings Consolidator
Inspects and in-place updates ~/.gemini/memory/learnings.md with verified technical invariants.
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

def consolidate_learning(topic_header: str, bullet_point: str, learnings_path: str = None) -> bool:
    if not learnings_path:
        learnings_file = Path(os.path.expanduser("~/.gemini/memory/learnings.md")).resolve()
    else:
        learnings_file = Path(learnings_path).resolve()

    if not learnings_file.exists():
        learnings_file.parent.mkdir(parents=True, exist_ok=True)
        learnings_file.write_text("# Assistant Machine Learnings & Technical Invariants\n\n", encoding="utf-8")

    content = learnings_file.read_text(encoding="utf-8")
    
    # Check if bullet already present
    if bullet_point.strip() in content:
        print(f"[OK] Invariant already recorded in {learnings_file.name}.")
        return True

    # Check if section header exists
    if f"## {topic_header}" in content:
        # In-place append under that section
        parts = content.split(f"## {topic_header}")
        new_content = parts[0] + f"## {topic_header}\n- {bullet_point.strip()}\n" + parts[1].lstrip("\n")
    else:
        # Create new section
        new_content = content.rstrip() + f"\n\n## {topic_header}\n- {bullet_point.strip()}\n"

    learnings_file.write_text(new_content, encoding="utf-8")
    print(f"[OK] Consolidated new invariant into '{topic_header}' in {learnings_file.name}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python consolidate_learnings.py <topic_header> <bullet_point> [learnings_file_path]")
        sys.exit(1)

    t_header = sys.argv[1]
    b_point = sys.argv[2]
    l_path = sys.argv[3] if len(sys.argv) > 3 else None
    consolidate_learning(t_header, b_point, l_path)
