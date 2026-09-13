import sys
import os
import sqlite3
from datetime import datetime, date, timedelta
import io

# Force UTF-8 stdout on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DB_PATH = os.path.expandvars(r"%APPDATA%\Campaigns\Database\campaigns.sqlite")

def get_db():
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at: {DB_PATH}")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA busy_timeout = 10000;")
    conn.row_factory = sqlite3.Row
    return conn

def parse_ddmmyyyy(date_str):
    try:
        parts = date_str.strip().split("-")
        return date(int(parts[2]), int(parts[1]), int(parts[0]))
    except Exception:
        return None

def list_active():
    conn = get_db()
    cur = conn.cursor()
    
    print("==================================================")
    print("⚔️ CAMPAIGNS COMMAND CENTER: ACTIVE THEATERS")
    print("==================================================")
    
    cur.execute("""
        SELECT id, title, priority, stage, deadline, initiated_at
        FROM Tasks
        WHERE state = 'Execution'
        ORDER BY id DESC
    """)
    tasks = cur.fetchall()
    
    print(f"\n⚡ Active Execution Campaigns ({len(tasks)}):")
    if not tasks:
        print("  *(No active campaigns in Execution theater)*")
    for t in tasks:
        cur.execute("SELECT tag_name FROM Tags WHERE task_id = ?", (t["id"],))
        tags = [r["tag_name"] for r in cur.fetchall()]
        tag_str = f"[{', '.join(tags)}]" if tags else ""
        
        cur.execute("SELECT status, count(*) as cnt FROM Subtasks WHERE task_id = ? GROUP BY status", (t["id"],))
        stats = {r["status"]: r["cnt"] for r in cur.fetchall()}
        comp = stats.get("Completed", 0)
        doing = stats.get("Doing", 0)
        init = stats.get("Initiated", 0)
        failed = stats.get("Failed", 0)
        total = comp + doing + init + failed
        
        print(f" - [{t['id']}] {t['title']} ({t['priority']}) {tag_str}")
        print(f"     📅 Deadline: {t['deadline'] or 'N/A'} | Stage: {t['stage']}")
        print(f"     📊 Subtasks: {comp}/{total} Completed ({doing} Doing, {failed} Failed, {init} Initiated)")

    strikes_radar("week")

def strikes_radar(scope="today"):
    conn = get_db()
    cur = conn.cursor()
    today = date.today()
    today_str = today.strftime("%d-%m-%Y")
    
    cur.execute("""
        SELECT id, title, execution_date, priority, status
        FROM Strikes
        ORDER BY id ASC
    """)
    all_strikes = cur.fetchall()
    
    today_strikes = []
    week_strikes = []
    pending_strikes = []
    
    for s in all_strikes:
        s_date = parse_ddmmyyyy(s["execution_date"])
        if not s_date:
            continue
            
        if s["status"] == "PENDING" or (s_date < today and s["status"] in ("STANDBY", "ENGAGED")):
            pending_strikes.append(s)
        elif s_date == today and s["status"] != "ABORTED":
            today_strikes.append(s)
        elif today <= s_date <= today + timedelta(days=7) and s["status"] != "ABORTED":
            week_strikes.append(s)

    if scope == "today":
        print("==================================================")
        print(f"🎯 DAILY STRIKE RADAR: {today_str}")
        print("==================================================")
        if pending_strikes:
            print(f"\n🚨 OVERDUE / PENDING STRIKES ({len(pending_strikes)}):")
            for s in pending_strikes:
                print(f" - 🔴 [{s['id']}] {s['execution_date']} | {s['status']:<10} | {s['title']} ({s['priority']})")
        print(f"\n⚡ TODAY'S SCHEDULED STRIKES ({len(today_strikes)}):")
        if not today_strikes:
            print("  *(No strikes scheduled specifically for today)*")
        for s in today_strikes:
            icon = "🔵" if s["status"] == "STANDBY" else ("🟡" if s["status"] == "ENGAGED" else "🟢")
            print(f" - {icon} [{s['id']}] {s['status']:<10} | {s['title']} ({s['priority']})")
        print("==================================================")
    else:
        print("==================================================")
        print(f"📅 7-DAY TACTICAL STRIKE RADAR ({today_str} to {(today + timedelta(days=7)).strftime('%d-%m-%Y')}):")
        print("==================================================")
        if pending_strikes:
            print(f"🚨 OVERDUE / PENDING ({len(pending_strikes)}):")
            for s in pending_strikes:
                print(f" - 🔴 [{s['id']}] {s['execution_date']} | {s['status']:<10} | {s['title']} ({s['priority']})")
            print()
        
        merged_week = today_strikes + week_strikes
        merged_week.sort(key=lambda x: parse_ddmmyyyy(x["execution_date"]) or today)
        if not merged_week:
            print("  *(No strikes in the next 7 days)*")
        for s in merged_week:
            icon = "🔴" if s["execution_date"] == today_str else "🔵"
            print(f" - {icon} [{s['id']}] {s['execution_date']} | {s['status']:<10} | {s['title']} ({s['priority']})")
        print("==================================================")

def check_collision(query):
    conn = get_db()
    cur = conn.cursor()
    words = [w.strip().lower() for w in query.split() if len(w.strip()) > 2]
    if not words:
        return
        
    print(f"🔍 Checking collision for keywords: {words}...")
    cur.execute("SELECT id, title, state, stage, priority, deadline FROM Tasks")
    tasks = cur.fetchall()
    
    matches = []
    for t in tasks:
        t_title_lower = t["title"].lower()
        matched_words = [w for w in words if w in t_title_lower]
        if matched_words:
            matches.append((t, matched_words))
            
    if matches:
        print(f"⚠️ POTENTIAL DUPLICATES FOUND ({len(matches)}):")
        for t, matched in matches:
            print(f" - [{t['id']}] {t['title']} (State: {t['state']} | Stage: {t['stage']} | Deadline: {t['deadline'] or 'N/A'})")
            print(f"     Matched keywords: {matched}")
    else:
        print("✅ No existing duplicate campaigns found. Clear to plan new target.")

def show_campaign(task_id):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM Tasks WHERE id = ?", (task_id,))
    t = cur.fetchone()
    if not t:
        print(f"❌ Campaign ID {task_id} not found.")
        return
        
    cur.execute("SELECT tag_name FROM Tags WHERE task_id = ?", (task_id,))
    tags = [r["tag_name"] for r in cur.fetchall()]
    
    print("==================================================")
    print(f"⚔️ CAMPAIGN [{t['id']}]: {t['title']}")
    print("==================================================")
    print(f"🏛️ State: {t['state']} | Stage: {t['stage']} | Priority: {t['priority']}")
    print(f"📅 Origin: {t['origin_date']} | Modified: {t['modification_date']} | Deadline: {t['deadline'] or 'N/A'}")
    print(f"🏷️ Tags: {', '.join(tags) if tags else 'None'}")
    if t["reschedule_count"] > 0:
        print(f"⚠️ Reschedules ({t['reschedule_count']}/2): R1={t['reschedule_1'] or 'N/A'}, R2={t['reschedule_2'] or 'N/A'}")
    
    print("\n📝 Tactical Subtasks:")
    cur.execute("SELECT id, title, status, creation_time FROM Subtasks WHERE task_id = ? ORDER BY id ASC", (task_id,))
    subs = cur.fetchall()
    if not subs:
        print("  *(No subtasks)*")
    for s in subs:
        st_icon = "[x]" if s["status"] == "Completed" else ("[~]" if s["status"] == "Doing" else ("[-]" if s["status"] == "Failed" else "[ ]"))
        print(f"  {st_icon} ({s['status']:<9}) #{s['id']} {s['title']}")
        
    print("\n==================================================")

def audit_db():
    conn = get_db()
    cur = conn.cursor()
    print("==================================================")
    print("🔍 CAMPAIGNS DATABASE INTEGRITY AUDIT")
    print("==================================================")
    
    cur.execute("SELECT count(*) FROM Tasks")
    total_tasks = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM Subtasks")
    total_subtasks = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM Strikes")
    total_strikes = cur.fetchone()[0]
    
    cur.execute("SELECT count(*) FROM Subtasks WHERE task_id NOT IN (SELECT id FROM Tasks)")
    orphaned_subs = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM Tags WHERE task_id NOT IN (SELECT id FROM Tasks)")
    orphaned_tags = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM Strikes WHERE subtask_id IS NOT NULL AND subtask_id NOT IN (SELECT id FROM Subtasks)")
    orphaned_strike_links = cur.fetchone()[0]
    
def show_progress(task_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, state, stage, deadline, priority FROM Tasks WHERE id = ?", (task_id,))
    t = cur.fetchone()
    if not t:
        print(f"❌ Campaign ID {task_id} not found.")
        return
        
    cur.execute("SELECT status, count(*) as cnt FROM Subtasks WHERE task_id = ? GROUP BY status", (task_id,))
    stats = {r["status"]: r["cnt"] for r in cur.fetchall()}
    comp = stats.get("Completed", 0)
    doing = stats.get("Doing", 0)
    init = stats.get("Initiated", 0)
    failed = stats.get("Failed", 0)
    total = comp + doing + init + failed
    
    pct = int((comp / total) * 100) if total > 0 else 0
    filled_len = int(pct / 5)  # 20 blocks
    bar = "█" * filled_len + "░" * (20 - filled_len)
    
    today = date.today()
    d_str = t["deadline"]
    days_left_str = ""
    if d_str:
        d_val = parse_ddmmyyyy(d_str)
        if d_val:
            diff = (d_val - today).days
            days_left_str = f"({diff} days remaining)" if diff >= 0 else f"(⚠️ {abs(diff)} DAYS OVERDUE)"
            
    print("==================================================")
    print(f"⚔️ {t['title']} [Task #{t['id']}]")
    print("==================================================")
    print(f"[{bar}] {pct}% Milestone Progress")
    print(f"📊 Breakdown: {comp}/{total} Completed | {doing} In Progress | {failed} Failed | {init} Planned")
    print(f"📅 Deadline: {d_str or 'N/A'} {days_left_str}")
    print(f"🏛️ State: {t['state']} | Stage: {t['stage']} | Priority: {t['priority']}")
    print("==================================================")

def inspect_breach():
    conn = get_db()
    cur = conn.cursor()
    today = date.today()
    
    print("==================================================")
    print("🚨 CAMPAIGNS BREACH & OVERDUE INSPECTOR")
    print("==================================================")
    
    cur.execute("""
        SELECT id, title, state, stage, deadline, reschedule_count
        FROM Tasks
        WHERE state IN ('Execution', 'Breach')
    """)
    tasks = cur.fetchall()
    
    overdue_tasks = []
    for t in tasks:
        d_val = parse_ddmmyyyy(t["deadline"])
        if d_val and d_val < today:
            overdue_tasks.append((t, (today - d_val).days))
            
    if not overdue_tasks:
        print("✅ Zero overdue campaigns detected! All execution deadlines intact.")
    else:
        print(f"⚠️ {len(overdue_tasks)} Campaign(s) Past Deadline:\n")
        for t, days in overdue_tasks:
            rc = t["reschedule_count"]
            rc_str = f"{rc}/2 Reschedules Used" if rc < 2 else "❌ MAX RESCHEDULES REACHED"
            print(f" - [{t['id']}] {t['title']}")
            print(f"     🔴 Overdue by: {days} days (Deadline was {t['deadline']})")
            print(f"     🏛️ Theater: {t['state']} | Reschedule Permits: {rc_str}")
    print("==================================================")

def read_strategy_notes(task_id):
    strategies_dir = os.path.expandvars(r"%USERPROFILE%\Obsidian\Adhipati\Campaigns")
    if not os.path.exists(strategies_dir):
        print(f"❌ Obsidian directory not found at: {strategies_dir}")
        return
        
    # Search for markdown file with Task Id: <task_id>
    found_file = None
    for root, _, files in os.walk(strategies_dir):
        for f in files:
            if f.endswith(".md"):
                fp = os.path.join(root, f)
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as mf:
                        header = mf.read(2048)
                        if f"Task Id: {task_id}" in header:
                            found_file = fp
                            break
                except Exception:
                    pass
        if found_file:
            break
            
    if not found_file:
        print(f"ℹ️ No materialized Obsidian strategy note found for Task ID #{task_id}.")
        print("   (Note will be generated on-demand when opened in the Campaigns UI app).")
        return
        
    print("==================================================")
    print(f"📖 STRATEGY INTEL NOTE: [Task #{task_id}]")
    print(f"📁 Path: {found_file}")
    print("==================================================")
    
    with open(found_file, "r", encoding="utf-8", errors="ignore") as mf:
        content = mf.read()
        
    sentinel = "<!-- @@CAMPAIGNS_NOTES_START@@"
    if sentinel in content:
        notes_part = content.split(sentinel, 1)[1]
        # Remove the first comment closing line if present
        if "-->" in notes_part:
            notes_part = notes_part.split("-->", 1)[1].strip()
        print(notes_part)
    else:
        print("*(No custom Zone 3 notes found below sentinel line)*")
    print("==================================================")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("list", "show_active"):
        list_active()
    elif sys.argv[1] == "today":
        strikes_radar("today")
    elif sys.argv[1] == "week":
        strikes_radar("week")
    elif sys.argv[1] == "check" and len(sys.argv) > 2:
        check_collision(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "audit":
        audit_db()
    elif sys.argv[1] == "breach":
        inspect_breach()
    elif sys.argv[1] == "progress" and len(sys.argv) > 2:
        show_progress(int(sys.argv[2]))
    elif sys.argv[1] == "read" and len(sys.argv) > 2:
        read_strategy_notes(int(sys.argv[2]))
    elif sys.argv[1] == "show" and len(sys.argv) > 2:
        show_campaign(int(sys.argv[2]))
    else:
        print("Usage: python campaign_helper.py [list | today | week | breach | progress <id> | read <id> | check <keyword> | audit | show <task_id>]")

if __name__ == "__main__":
    main()

