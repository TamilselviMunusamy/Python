import tkinter as tk
from tkinter import messagebox
from utils.parser import parse_task
from services.task_service import load_tasks, save_tasks
from utils.api import get_quote
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Smart To-Do List Pro")
        self.root.geometry("600x600")

        self.tasks = load_tasks()

        self.setup_ui()
        self.update_list()

    def setup_ui(self):
        tk.Label(self.root, text="Smart To-Do List", font=("Arial", 16, "bold")).pack(pady=10)

        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(pady=5)

        tk.Button(self.root, text="Add Task", command=self.add_task).pack()
        
        tk.Button(self.root, text="💡 Get Motivation", command=get_quote).pack(pady=5)

        self.search_entry = tk.Entry(self.root, width=40)
        self.search_entry.pack(pady=5)

        tk.Button(self.root, text="Search", command=self.search_task).pack()
        tk.Button(self.root, text="Clear Search", command=self.clear_search).pack()

        self.listbox = tk.Listbox(self.root, width=80, height=20)
        self.listbox.pack(pady=10)

        self.listbox.bind("<Double-Button-1>", self.open_notes)

        frame = tk.Frame(self.root)
        frame.pack()

        tk.Button(frame, text="Delete", command=self.delete_task).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Mark Complete", command=self.mark_complete).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Clear All", command=self.clear_all).grid(row=0, column=2, padx=5)

    def add_task(self):
        text = self.entry.get().strip()
        if not text:
            return

        task = parse_task(text)
        self.tasks.append(task)
        save_tasks(self.tasks)
        self.update_list()
        self.entry.delete(0, tk.END)

    def update_list(self, filtered=None):
        self.listbox.delete(0, tk.END)
        display_tasks = filtered if filtered else self.tasks

        for t in display_tasks:
            status = "✔" if t["completed"] else "✘"
            line = f"{status} {t['task']} | {t['time']} | {t['priority']} | {t['category']}"
            self.listbox.insert(tk.END, line)

    def delete_task(self):
        idx = self.listbox.curselection()
        if not idx:
            return
        self.tasks.pop(idx[0])
        save_tasks(self.tasks)
        self.update_list()

    def mark_complete(self):
        idx = self.listbox.curselection()
        if not idx:
            return
        self.tasks[idx[0]]["completed"] = True
        save_tasks(self.tasks)
        self.update_list()

    def search_task(self):
        keyword = self.search_entry.get().lower()
        filtered = [t for t in self.tasks if keyword in t["task"].lower()]
        self.update_list(filtered)

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.update_list()

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Delete all tasks?"):
            self.tasks.clear()
            save_tasks(self.tasks)
            self.update_list()

    def open_notes(self, event):
        idx = self.listbox.curselection()
        if not idx:
            return

        task = self.tasks[idx[0]]

        win = tk.Toplevel(self.root)
        win.title("Task Notes")
        win.geometry("400x300")

        tk.Label(win, text=task["task"], wraplength=350).pack(pady=5)

        text_area = tk.Text(win, height=10, width=40)
        text_area.pack()

        text_area.insert(tk.END, task.get("notes", ""))

        def save_note():
            task["notes"] = text_area.get("1.0", tk.END).strip()
            save_tasks(self.tasks)
            messagebox.showinfo("Saved", "Notes updated!")

        tk.Button(win, text="Save", command=save_note).pack()