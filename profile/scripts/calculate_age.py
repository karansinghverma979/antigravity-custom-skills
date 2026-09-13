import sys
import os
from datetime import datetime, date

# Force UTF-8 on Windows stdout
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DOB = date(2005, 8, 18)

def parse_date(date_str):
    for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Could not parse date: {date_str}. Use DD-MM-YYYY or YYYY-MM-DD.")

def calculate_age_breakdown(born, target):
    years = target.year - born.year
    months = target.month - born.month
    days = target.day - born.day

    if days < 0:
        months -= 1
        prev_month = target.month - 1 if target.month > 1 else 12
        prev_year = target.year if target.month > 1 else target.year - 1
        if prev_month in (1, 3, 5, 7, 8, 10, 12):
            prev_days = 31
        elif prev_month in (4, 6, 9, 11):
            prev_days = 30
        else:
            prev_days = 29 if (prev_year % 4 == 0 and (prev_year % 100 != 0 or prev_year % 400 == 0)) else 28
        days += prev_days

    if months < 0:
        years -= 1
        months += 12

    return years, months, days

def main():
    target = date.today()
    target_str = "Today (" + target.strftime("%d-%m-%Y") + ")"
    if len(sys.argv) > 1:
        target_input = sys.argv[1].strip()
        target = parse_date(target_input)
        target_str = target.strftime("%d-%m-%Y")
    
    years, months, days = calculate_age_breakdown(DOB, target)
    total_days = (target - DOB).days

    print("==================================================")
    print("👤 Candidate: Karan Singh Verma")
    print(f"📅 Date of Birth: {DOB.strftime('%d-%m-%Y')}")
    print(f"🎯 Reference / Cutoff Date: {target_str}")
    print(f"⏱️ Exact Age: {years} Years, {months} Months, {days} Days ({total_days} total days)")
    print("==================================================")
    print("📋 Common Recruitment Eligibility Windows:")
    windows = [
        ("18 - 23 (SSC GD, Defense Soldier)", 18, 23),
        ("18 - 25 (SSC MTS, Delhi Police, CHSL Lower)", 18, 25),
        ("18 - 27 (SSC CHSL / CGL General Lower)", 18, 27),
        ("20 - 25 (CPO SI, CAPF AC)", 20, 25),
        ("21 - 30 (SSC CGL Upper, State PCS / Desk)", 21, 30),
        ("21 - 32 (Civil Services / UPSC CSE)", 21, 32),
    ]
    for label, min_age, max_age in windows:
        if years < min_age:
            status = "⏳ NOT YET (Underage)"
        elif years > max_age or (years == max_age and (months > 0 or days > 0)):
            status = "❌ EXPIRED (Overage)"
        else:
            status = "✅ ELIGIBLE"
        print(f" - {label:<44}: {status}")
    print("==================================================")

if __name__ == "__main__":
    main()
