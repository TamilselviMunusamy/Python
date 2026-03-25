import tkinter as tk
from tkinter import messagebox
import re
import json
from datetime import datetime, timedelta

FILE_NAME = "tasks.json"

def load_tasks():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except:
        return []

def save_tasks():
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)


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



def open_notes(event):
    idx = listbox.curselection()
    if not idx:
        return

    index = idx[0]
    task = tasks[index]

    note_window = tk.Toplevel(root)
    note_window.title("Task Notes")
    note_window.geometry("400x300")

    tk.Label(note_window, text="Task:", font=("Arial", 10, "bold")).pack()
    tk.Label(note_window, text=task["task"], wraplength=350).pack(pady=5)

    tk.Label(note_window, text="Notes:", font=("Arial", 10, "bold")).pack()

    text_area = tk.Text(note_window, height=10, width=40)
    text_area.pack(pady=5)

   
    text_area.insert(tk.END, task.get("notes", ""))

    def save_note():
        task["notes"] = text_area.get("1.0", tk.END).strip()
        save_tasks()
        messagebox.showinfo("Saved", "Notes updated!")

    tk.Button(note_window, text="Save Notes", command=save_note).pack(pady=5)

def add_task():
    text = entry.get().strip()
    if not text:
        return

    task = parse_task(text)
    tasks.append(task)
    save_tasks()
    update_list()
    entry.delete(0, tk.END)

def update_list(filtered=None):
    listbox.delete(0, tk.END)
    display_tasks = filtered if filtered else tasks

    for i, t in enumerate(display_tasks):
        status = "✔" if t["completed"] else "✘"
        line = f"{status} {t['task']} | {t['time']} | {t['priority']} | {t['category']}"
        listbox.insert(tk.END, line)

def delete_task():
    idx = listbox.curselection()
    if not idx:
        return
    tasks.pop(idx[0])
    save_tasks()
    update_list()

def mark_complete():
    idx = listbox.curselection()
    if not idx:
        return
    tasks[idx[0]]["completed"] = True
    save_tasks()
    update_list()

def search_task():
    keyword = search_entry.get().lower()
    filtered = [t for t in tasks if keyword in t["task"].lower()]
    update_list(filtered)

def clear_search():
    search_entry.delete(0, tk.END)
    update_list()

def clear_all():
    if messagebox.askyesno("Confirm", "Delete all tasks?"):
        tasks.clear()
        save_tasks()
        update_list()


tasks = load_tasks()

root = tk.Tk()
root.title("🚀 Smart To-Do List Pro")
root.geometry("600x600")

tk.Label(root, text="Smart To-Do List", font=("Arial", 16, "bold")).pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

tk.Button(root, text="Add Task", command=add_task).pack()


search_entry = tk.Entry(root, width=40)
search_entry.pack(pady=5)

tk.Button(root, text="Search", command=search_task).pack()
tk.Button(root, text="Clear Search", command=clear_search).pack()

listbox = tk.Listbox(root, width=80, height=20)
listbox.pack(pady=10)
listbox.bind("<<ListboxSelect>>", open_notes)

frame = tk.Frame(root)
frame.pack()

tk.Button(frame, text="Delete", command=delete_task).grid(row=0, column=0, padx=5)
tk.Button(frame, text="Mark Complete", command=mark_complete).grid(row=0, column=1, padx=5)
tk.Button(frame, text="Clear All", command=clear_all).grid(row=0, column=2, padx=5)

update_list()
root.mainloop()