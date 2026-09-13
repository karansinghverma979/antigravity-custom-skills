#!/usr/bin/env python3
"""
Hook Master Generator
Scaffolds compliant Antigravity lifecycle hook handlers and hooks.json configurations.
"""

import sys
import json
from pathlib import Path

HOOK_HANDLER_TEMPLATE = '''#!/usr/bin/env python3
"""
{hook_name} - Antigravity Lifecycle Hook Handler ({event_type})
"""

import sys
import json

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def main():
    try:
        input_data = json.load(sys.stdin)
    except Exception:
        input_data = {{}}

    # Implement custom hook logic here:
{hook_logic}

    # Output response
    print(json.dumps(response))

if __name__ == "__main__":
    main()
'''

PRE_TOOL_LOGIC = '''    tool_call = input_data.get("toolCall", {})
    tool_name = tool_call.get("name", "")
    args = tool_call.get("args", {})

    # Default: allow
    response = {
        "decision": "allow"
    }

    # Example safety gate:
    # if "rm -rf" in args.get("CommandLine", ""):
    #     response = {"decision": "deny", "reason": "Blocked unsafe deletion."}
'''

STOP_LOGIC = '''    # Check if stop should be prevented
    # Example: return {"decision": "continue", "reason": "Background task pending"}
    response = {}
'''

def scaffold_hook(target_dir: str, hook_name: str, event_type: str = "PreToolUse") -> bool:
    out_dir = Path(target_dir).resolve()
    scripts_dir = out_dir / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)

    script_path = scripts_dir / f"{hook_name}.py"
    logic = PRE_TOOL_LOGIC if event_type in ["PreToolUse", "PostToolUse"] else STOP_LOGIC

    script_path.write_text(
        HOOK_HANDLER_TEMPLATE.format(hook_name=hook_name, event_type=event_type, hook_logic=logic),
        encoding="utf-8"
    )

    hooks_json_path = out_dir / "hooks.json"
    hooks_data = {}
    if hooks_json_path.exists():
        try:
            hooks_data = json.loads(hooks_json_path.read_text(encoding="utf-8"))
        except Exception:
            hooks_data = {}

    if event_type in ["PreToolUse", "PostToolUse"]:
        hooks_data[hook_name] = {
            event_type: [
                {
                    "matcher": "run_command",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"python ./scripts/{hook_name}.py",
                            "timeout": 30
                        }
                    ]
                }
            ]
        }
    else:
        hooks_data[hook_name] = {
            event_type: [
                {
                    "type": "command",
                    "command": f"python ./scripts/{hook_name}.py",
                    "timeout": 30
                }
            ]
        }

    hooks_json_path.write_text(json.dumps(hooks_data, indent=2), encoding="utf-8")
    print(f"[OK] Hook '{hook_name}' ({event_type}) scaffolded at {out_dir}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_hook.py <target_directory> <hook_name> [PreToolUse|PostToolUse|PreInvocation|PostInvocation|Stop]")
        sys.exit(1)
    
    tgt = sys.argv[1]
    name = sys.argv[2]
    evt = sys.argv[3] if len(sys.argv) > 3 else "PreToolUse"
    scaffold_hook(tgt, name, evt)
