import sys
import os
import sqlite3
import shutil
import json
import re
from datetime import datetime, date
import io

# Force UTF-8 on Windows stdout
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DB_PATH = os.path.expandvars(r"%APPDATA%\Campaigns\Database\campaigns.sqlite")
BAK_PATH = os.path.expandvars(r"%APPDATA%\Campaigns\Database\campaigns.sqlite.bak")

def is_valid_ddmmyyyy(date_str):
    if not date_str or not isinstance(date_str, str):
        return False
    parts = date_str.strip().split("-")
    if len(parts) != 3:
        return False
    d, m, y = parts
    if len(d) != 2 or len(m) != 2 or len(y) != 4:
        return False
    try:
        dt = datetime(int(y), int(m), int(d))
        return True
    except ValueError:
        return False

def get_today_ddmmyyyy():
    return date.today().strftime("%d-%m-%Y")

def get_db():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}")
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA busy_timeout = 10000;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def backup_db():
    if os.path.exists(DB_PATH):
        shutil.copy2(DB_PATH, BAK_PATH)
        print(f"💾 Snapshot backup created: {BAK_PATH}")

def restore_backup():
    if not os.path.exists(BAK_PATH):
        print("❌ No backup snapshot found to restore.")
        sys.exit(1)
    shutil.copy2(BAK_PATH, DB_PATH)
    print("✅ Database successfully restored from backup snapshot!")

def insert_campaign(payload_json):
    try:
        data = json.loads(payload_json) if isinstance(payload_json, str) else payload_json
    except Exception as e:
        print(f"❌ Invalid JSON payload: {e}")
        sys.exit(1)

    title = data.get("title", "").strip()
    if not title:
        print("❌ Error: Campaign title is required.")
        sys.exit(1)

    origin_date = data.get("origin_date", get_today_ddmmyyyy())
    if not is_valid_ddmmyyyy(origin_date):
        origin_date = get_today_ddmmyyyy()

    priority = data.get("priority", "Medium")
    if priority not in ("High", "Medium", "Low"):
        priority = "Medium"

    state = data.get("state", "Execution")
    if state not in ("Arsenal", "Execution", "Breach", "Archive"):
        state = "Execution"

    stage = data.get("stage")
    if not stage:
        stage = "Active" if state == "Execution" else ("RawIntel" if state == "Arsenal" else "Overdue")

    deadline = data.get("deadline")
    if state == "Execution" and (not deadline or not is_valid_ddmmyyyy(deadline)):
        print("❌ Error: Valid deadline (DD-MM-YYYY) is required for Execution state.")
        sys.exit(1)

    initiated_at = data.get("initiated_at", get_today_ddmmyyyy() if state == "Execution" else None)
    tags = [t.strip().upper() for t in data.get("tags", []) if t.strip()]
    subtasks = data.get("subtasks", [])
    strikes = data.get("strikes", [])

    backup_db()
    conn = get_db()
    
    try:
        with conn:
            cur = conn.cursor()
            
            # Insert Task
            cur.execute("""
                INSERT INTO Tasks (title, origin_date, modification_date, priority, state, stage, deadline, initiated_at, reschedule_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
            """, (title, origin_date, origin_date, priority, state, stage, deadline, initiated_at))
            task_id = cur.lastrowid
            
            # Insert Tags
            for tag in tags:
                cur.execute("INSERT INTO Tags (task_id, tag_name) VALUES (?, ?)", (task_id, tag))
                
            # Insert Subtasks
            subtask_id_map = {}
            for idx, sub in enumerate(subtasks):
                sub_title = sub.get("title", "").strip() if isinstance(sub, dict) else str(sub).strip()
                sub_status = sub.get("status", "Initiated") if isinstance(sub, dict) else "Initiated"
                if sub_status not in ("Initiated", "Doing", "Completed", "Failed"):
                    sub_status = "Initiated"
                sub_creation = sub.get("creation_time", origin_date) if isinstance(sub, dict) else origin_date
                
                cur.execute("""
                    INSERT INTO Subtasks (task_id, title, creation_time, status)
                    VALUES (?, ?, ?, ?)
                """, (task_id, sub_title, sub_creation, sub_status))
                subtask_id_map[idx] = cur.lastrowid
                
            # Insert Strikes
            for stk in strikes:
                stk_title = stk.get("title", "").strip()
                if not stk_title:
                    continue
                stk_exec = stk.get("execution_date", origin_date)
                if not is_valid_ddmmyyyy(stk_exec):
                    stk_exec = origin_date
                stk_priority = stk.get("priority", "Medium")
                stk_status = stk.get("status", "STANDBY")
                stk_notes = stk.get("notes", "")
                sub_ref_idx = stk.get("subtask_index")
                linked_sub_id = subtask_id_map.get(sub_ref_idx) if sub_ref_idx is not None else stk.get("subtask_id")
                
                cur.execute("""
                    INSERT INTO Strikes (title, created_at, execution_date, priority, status, notes, subtask_id, reschedule_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 0)
                """, (stk_title, origin_date, stk_exec, stk_priority, stk_status, stk_notes, linked_sub_id))

        print(f"==================================================")
        print(f"✅ Campaign Successfully Inserted! (Task ID: {task_id})")
        print(f"⚔️ Title: {title}")
        print(f"🏛️ State: {state} | Stage: {stage} | Priority: {priority}")
        print(f"📅 Deadline: {deadline or 'N/A'}")
        print(f"🏷️ Tags: {', '.join(tags) if tags else 'None'}")
        print(f"📝 Subtasks Added: {len(subtasks)}")
        print(f"⚡ Strikes Scheduled: {len(strikes)}")
        print(f"🔄 Tip: Press 'Ctrl + R' in the Campaigns UI app to refresh view immediately.")
        print(f"==================================================")

    except Exception as e:
        print(f"❌ Database Transaction Failed: {e}")
        print("Rolling back to backup snapshot...")
        restore_backup()
        sys.exit(1)

def insert_strike(title_raw, exec_date_raw=None, priority_raw="Medium", notes=""):
    today_str = get_today_ddmmyyyy()
    
    # Priority hashtag extraction
    priority = "Medium"
    clean_title = title_raw
    if "#High" in clean_title or "#high" in clean_title or "#HIGH" in clean_title:
        priority = "High"
        clean_title = re.sub(r'#high|#High|#HIGH', '', clean_title)
    elif "#Low" in clean_title or "#low" in clean_title or "#LOW" in clean_title:
        priority = "Low"
        clean_title = re.sub(r'#low|#Low|#LOW', '', clean_title)
    elif "#Med" in clean_title or "#med" in clean_title or "#Medium" in clean_title:
        priority = "Medium"
        clean_title = re.sub(r'#med|#Med|#Medium', '', clean_title)
        
    if priority_raw in ("High", "Medium", "Low"):
        priority = priority_raw
        
    clean_title = clean_title.strip()
    if not clean_title:
        print("❌ Error: Strike title cannot be empty.")
        sys.exit(1)
        
    exec_date = exec_date_raw if (exec_date_raw and is_valid_ddmmyyyy(exec_date_raw)) else today_str
    
    backup_db()
    conn = get_db()
    try:
        with conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Strikes (title, created_at, execution_date, priority, status, notes, subtask_id, reschedule_count)
                VALUES (?, ?, ?, ?, 'STANDBY', ?, NULL, 0)
            """, (clean_title, today_str, exec_date, priority, notes.strip()))
            strike_id = cur.lastrowid
            
        print("==================================================")
        print(f"✅ Strike Successfully Scheduled! (Strike ID: {strike_id})")
        print(f"🎯 Title: {clean_title}")
        print(f"📅 Target Execution Date: {exec_date}")
        print(f"⚡ Priority: {priority} | Status: STANDBY")
        print(f"🔄 Press 'Ctrl + R' in Campaigns app to view.")
        print("==================================================")
    except Exception as e:
        print(f"❌ Failed to insert strike: {e}")
        restore_backup()
        sys.exit(1)

def update_strike_status(strike_id, new_status):
    valid_statuses = {
        "done": "NEUTRALIZED",
        "neutralized": "NEUTRALIZED",
        "engage": "ENGAGED",
        "engaged": "ENGAGED",
        "standby": "STANDBY",
        "abort": "ABORTED",
        "aborted": "ABORTED"
    }
    target_status = valid_statuses.get(new_status.lower().strip())
    if not target_status:
        print(f"❌ Invalid status '{new_status}'. Allowed: done, engage, standby, abort")
        sys.exit(1)
        
    backup_db()
    conn = get_db()
    try:
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT id, title, status FROM Strikes WHERE id = ?", (strike_id,))
            stk = cur.fetchone()
            if not stk:
                print(f"❌ Strike ID {strike_id} not found.")
                sys.exit(1)
                
            cur.execute("UPDATE Strikes SET status = ? WHERE id = ?", (target_status, strike_id))
            
        print("==================================================")
        print(f"✅ Strike #{strike_id} Status Updated!")
        print(f"🎯 Title: {stk[1]}")
        print(f"⚡ Previous: {stk[2]} ➔ New: {target_status}")
        print(f"🔄 Press 'Ctrl + R' in Campaigns app to sync.")
        print("==================================================")
    except Exception as e:
        print(f"❌ Failed to update strike: {e}")
        restore_backup()
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python campaign_writer.py [insert <json_payload> | strike <title> [date] [priority] [notes] | status <id> <done|engage|abort|standby> | restore]")
        sys.exit(1)
        
    cmd = sys.argv[1]
    if cmd == "restore":
        restore_backup()
    elif cmd == "insert" and len(sys.argv) > 2:
        payload = sys.argv[2]
        insert_campaign(payload)
    elif cmd == "strike" and len(sys.argv) > 2:
        title = sys.argv[2]
        exec_d = sys.argv[3] if len(sys.argv) > 3 else None
        prio = sys.argv[4] if len(sys.argv) > 4 else "Medium"
        nts = sys.argv[5] if len(sys.argv) > 5 else ""
        insert_strike(title, exec_d, prio, nts)
    elif cmd == "status" and len(sys.argv) > 3:
        s_id = int(sys.argv[2])
        st = sys.argv[3]
        update_strike_status(s_id, st)
    else:
        print("Unknown command. Use 'insert', 'strike', 'status', or 'restore'.")

if __name__ == "__main__":
    main()


