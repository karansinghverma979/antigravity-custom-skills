#!/usr/bin/env python3
"""
Trajectory Harvester
Scans Antigravity transcript logs to detect friction points, tool call failures,
and candidate learnings for self-evolution.
"""

import sys
import os
import json
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def harvest_trajectories(brain_dir_path: str = None) -> list:
    if not brain_dir_path:
        brain_dir = Path(os.path.expanduser("~/.gemini/antigravity-cli/brain")).resolve()
    else:
        brain_dir = Path(brain_dir_path).resolve()

    if not brain_dir.is_dir():
        print(f"[ERROR] Brain directory '{brain_dir}' does not exist.")
        return []

    print(f"[*] Harvesting execution trajectories from: {brain_dir}")
    friction_events = []

    # Find all transcript.jsonl files
    transcript_files = list(brain_dir.glob("*/.system_generated/logs/transcript.jsonl"))
    print(f"[*] Found {len(transcript_files)} conversation transcript(s).")

    # Inspect the most recent 10 sessions
    for tf in sorted(transcript_files, key=lambda f: f.stat().st_mtime, reverse=True)[:10]:
        conv_id = tf.parent.parent.parent.name
        try:
            with open(tf, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    step = json.loads(line)
                    status = step.get("status", "")
                    step_type = step.get("type", "")

                    if status == "ERROR":
                        content = str(step.get("content", ""))
                        friction_events.append({
                            "conversationId": conv_id,
                            "type": "TOOL_ERROR",
                            "step_index": step.get("step_index"),
                            "snippet": content[:300]
                        })
        except Exception:
            pass

    print(f"\n[RESULT] Harvested {len(friction_events)} friction event(s) across recent trajectories.")
    for ev in friction_events[:5]:
        print(f"  - [{ev['type']}] Conv {ev['conversationId'][:8]}... Step {ev['step_index']}: {ev['snippet'][:120]}...")

    return friction_events

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    harvest_trajectories(target)
