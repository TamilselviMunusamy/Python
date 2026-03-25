import re
from datetime import datetime, timedelta

def parse_task(text):
    task = {
        "task": text,
        "time": "No deadline",
        "priority": "Medium",
        "category": "General",
        "completed": False,
        "notes": ""
    }

    lower = text.lower()
    date = datetime.now()

    if "tomorrow" in lower:
        date += timedelta(days=1)

    weekdays = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    for i, day in enumerate(weekdays):
        if f"next {day}" in lower:
            today = datetime.now().weekday()
            diff = (i - today + 7) % 7
            diff = diff if diff != 0 else 7
            date += timedelta(days=diff)

    match_date = re.search(r"\d{4}-\d{2}-\d{2}", text)
    if match_date:
        try:
            date = datetime.strptime(match_date.group(), "%Y-%m-%d")
        except:
            pass

    match_time = re.search(r"(\d{1,2})(am|pm)", lower)
    if match_time:
        hour = int(match_time.group(1))
        if match_time.group(2) == "pm" and hour != 12:
            hour += 12
        if match_time.group(2) == "am" and hour == 12:
            hour = 0
        date = date.replace(hour=hour, minute=0)

    task["time"] = date.strftime("%Y-%m-%d %H:%M")

    if "high" in lower:
        task["priority"] = "High"
    elif "low" in lower:
        task["priority"] = "Low"

    if "work" in lower:
        task["category"] = "Work"
    elif "study" in lower:
        task["category"] = "Study"
    elif "personal" in lower:
        task["category"] = "Personal"

    return task