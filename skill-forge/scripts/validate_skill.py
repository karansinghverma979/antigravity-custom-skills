#!/usr/bin/env python3
"""
Antigravity Skill Validator
Validates skill directory layout, YAML frontmatter, line limits, and relative link integrity.
Fully Windows cp1252 / UTF-8 safe.
"""

import sys
import os
import re
from pathlib import Path

# Force UTF-8 on Windows stdout/stderr streams
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def validate_skill(skill_dir_path: str) -> bool:
    skill_dir = Path(skill_dir_path).resolve()
    if not skill_dir.is_dir():
        print(f"[ERROR] '{skill_dir}' is not a directory.")
        return False

    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        print(f"[ERROR] Missing 'SKILL.md' in '{skill_dir}'.")
        return False

    print(f"[*] Validating Skill: {skill_dir.name} ({skill_file})")
    has_errors = False
    warnings = []

    try:
        content = skill_file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[ERROR] Failed reading SKILL.md: {e}")
        return False

    lines = content.splitlines()

    # 1. Check Line Count (<500 lines recommended for progressive disclosure)
    if len(lines) > 500:
        warnings.append(f"SKILL.md has {len(lines)} lines (exceeds recommended 500-line progressive limit). Consider splitting into references/.")
    else:
        print(f"  [OK] Line Count: {len(lines)} lines (Within 500-line budget)")

    # 2. Check YAML Frontmatter
    frontmatter_match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", content, re.DOTALL)
    if not frontmatter_match:
        print("[ERROR] SKILL.md must start with a valid YAML frontmatter block (--- ... ---).")
        return False

    frontmatter_text = frontmatter_match.group(1)
    
    # Check name
    name_match = re.search(r"^name:\s*([a-z0-9\-_]+)\s*$", frontmatter_text, re.MULTILINE)
    if not name_match:
        print("[ERROR] Frontmatter missing valid 'name:' field (lowercase, numbers, dashes, underscores only).")
        has_errors = True
    else:
        skill_name = name_match.group(1)
        print(f"  [OK] Name: '{skill_name}'")
        if skill_name != skill_dir.name and skill_name != skill_dir.name.lower():
            warnings.append(f"Skill name '{skill_name}' does not match directory name '{skill_dir.name}'.")

    # Check description
    desc_match = re.search(r"^description:\s*(?:>-\s*|\"|')(.*)", frontmatter_text, re.MULTILINE)
    if not desc_match and "description:" not in frontmatter_text:
        print("[ERROR] Frontmatter missing required 'description:' field.")
        has_errors = True
    else:
        print("  [OK] Description: Present and formatted")

    # 3. Check Relative Markdown Links
    relative_links = re.findall(r"\[([^\]]+)\]\((?!http://|https://|mailto:|#)([^\)]+)\)", content)
    for label, link in relative_links:
        # Strip anchors if present
        clean_link = link.split("#")[0]
        if not clean_link:
            continue
        target_path = (skill_dir / clean_link).resolve()
        if not target_path.exists():
            warnings.append(f"Broken relative link '[{label}]({link})': Target '{target_path}' does not exist.")
        else:
            print(f"  [OK] Link verified: {clean_link}")

    # Report Warnings & Result
    if warnings:
        for w in warnings:
            print(f"  [WARN] {w}")

    if has_errors:
        print("\n[RESULT] Skill validation FAILED.")
        return False
    else:
        print("\n[RESULT] Skill validation PASSED successfully.")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        target = Path(__file__).parent.parent
    else:
        target = Path(sys.argv[1])
    
    success = validate_skill(str(target))
    sys.exit(0 if success else 1)
