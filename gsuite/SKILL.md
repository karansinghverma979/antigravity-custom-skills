---
name: gsuite
description: Executive command center, automation hub, and autonomous operational governor for Karan's Google Workspace ecosystem (Calendar, Tasks, Gmail, Drive, Docs, Sheets, Contacts) powered by the native google-workspace MCP server.
trigger: /gsuite
---

# 🌐 Google Workspace (`/gsuite`) Executive Command Center & Governance

Use this skill whenever Karan invokes `/gsuite`, `/gworkspace`, `/gtask`, `/gcontact`, `/gdoc`, or manages any aspect of his Google Workspace cloud ecosystem.

> **Single Source of Truth**: This skill is the authoritative operating governor, intent de-noiser, and execution bridge for Karan's Google Workspace suite, interfaced directly via the open-source [`antigravity-google-workspace`](https://github.com/karansinghverma979/antigravity-google-workspace) MCP server (`~/.gemini/google-workspace/server.py`).

---

## 🏛️ Operating Philosophy & Core Directives

### 0. 🛑 STRICT MCP-ONLY EXECUTION (Zero Ad-Hoc Scripts / Zero Direct REST Hackery)
* **ABSOLUTE BAN ON AD-HOC SCRIPTS**: The assistant is **strictly forbidden** from writing or running temporary background Python scripts (`scratch/*.py`, `python -c ...`) to interact with Google Workspace APIs.
* **MANDATORY DIRECT MCP TOOL CALLS**: Every query, task completion, contact update, email draft, calendar event, doc inspection, and drive search **MUST** execute exclusively via the native `google-workspace` MCP server.
* **Native Tool Whitelist (22 Operations)**:
  - **Tasks**: `gtasks_list_tasks`, `gtasks_create_task`, `gtasks_complete_task`, `gtasks_delete_task`
  - **Contacts**: `gcontacts_list`, `gcontacts_create`
  - **Docs**: `gdocs_create_doc`, `gdocs_read_doc`, `gdocs_append_text`
  - **Sheets**: `gsheets_read_range`, `gsheets_append_row`, `gsheets_update_range`
  - **Drive**: `gdrive_search_files`, `gdrive_read_file`, `gdrive_trash_file`
  - **Gmail**: `gmail_list_messages`, `gmail_get_message`, `gmail_create_draft`, `gmail_send_message`, `gmail_trash_message`
  - **Calendar**: `gcal_list_events`, `gcal_create_event`, `gcal_delete_event`

---

### 1. ⚡ Raw Velocity Intent Translation & De-Noising
* **Input Reality**: Karan operates at high velocity, providing raw shorthand, fragmented thoughts, voice-typed phrases, or immediate directives.
* **Extraction Protocol**:
  - Automatically isolate the target service (Tasks vs Contacts vs Drive vs Docs vs Gmail).
  - Normalize dates, times, contact names, and task statuses instantly.
  - Automatically match shorthand titles to existing task or document records.

---

### 2. 🪝 Pre-Execution 3-Point Confirmation Protocol (State-Altering Operations)
* **Mandatory Alignment**: Before executing destructive actions (deleting tasks, trashing emails/files) or batch mutations (>5 records):
  1. **🎯 Target Scope**: Exact Google service, list/folder ID, and record IDs being touched.
  2. **🧠 Translated Objective**: Crystal-clear distillation of the user's intent.
  3. **⚡ Action Plan & Payload Preview**: Step-by-step summary of mutations and any risk notices.
* **Fast-Path Read Exemption**: Pure reads, searches, and single-task completions execute immediately with zero friction.

---

### 3. 🧠 Self-Evolution & Learned Operational Invariants
* **Contact Taxonomy**: `RUDSETI` is the standard canonical prefix for all vocational institute peers and faculty (never `RUDSET`).
* **Task List Separation**:
  - `Co-worker` (`M1JSbkpUVXBKWGRCbnF5bw`): Dedicated to systems development, AI architectures, Antigravity skills, MCP servers, and codebase tasks.
  - `Reminder` (`MDE4NzQ3NTgwNjE4MzA1OTY3NDU6MDow`): Personal life theater, family logistics, financial reminders, purchases, and exam tracking.
* **Terminal Presentation Invariant**:
  - Never render Unicode box-drawing tables or complex ASCII frames in terminal output to prevent syntax highlighting distortions in Tokyo Night theme. Use clean standard markdown bullet points.

---

## 🎮 Invocation Commands & Shorthand Suite

| Command / Shorthand | Target Service | MCP Action Executed |
| :--- | :--- | :--- |
| **`/gsuite task list [coworker \| reminder]`** | Google Tasks | Calls `gtasks_list_tasks` with target list ID. |
| **`/gsuite task done <title \| id>`** | Google Tasks | Calls `gtasks_complete_task` on matching task. |
| **`/gsuite task add <title> [@date] [#list]`** | Google Tasks | Calls `gtasks_create_task` with parsed due date and list. |
| **`/gsuite contact search <name>`** | Google Contacts | Calls `gcontacts_list` and filters for matches. |
| **`/gsuite doc search <keyword>`** | Google Drive / Docs | Calls `gdrive_search_files` / `gdocs_read_doc`. |
| **`/gsuite mail unread`** | Gmail | Calls `gmail_list_messages` with query `is:unread`. |
| **`/gsuite cal today`** | Google Calendar | Calls `gcal_list_events` for today's timeline. |

---

## 🔄 Self-Learning Log & Rule Updates
*(Learnings, custom preferences, and workflow optimizations discovered during operations are preserved here in-place).*

- **12-09-2026**: Initial skill materialized. Token persistence verified under `~/.gemini/google-workspace/token.json` with multi-scope auto-refresh. Batch contact naming standardized to `RUDSETI`.
