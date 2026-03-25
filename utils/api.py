import requests
from tkinter import messagebox

def get_quote():
    try:
        res = requests.get("https://api.quotable.io/random")
        data = res.json()
        messagebox.showinfo("Motivation", data["content"])
    except:
        messagebox.showerror("Error", "API failed")