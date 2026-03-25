import requests
from tkinter import messagebox
import random

def get_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=3)
        response.raise_for_status()  # Raises error if bad response

        data = response.json()
        quote = data[0]["q"]
        author = data[0]["a"]

    except Exception:
        # 🔥 Offline fallback (ALWAYS works)
        offline_quotes = [
            ("Stay hungry, stay foolish.", "Steve Jobs"),
            ("Believe you can and you're halfway there.", "Roosevelt"),
            ("Push yourself, because no one else will.", "Unknown"),
            ("Dream big. Start small. Act now.", "Unknown"),
            ("Consistency is the key to success.", "Unknown")
        ]

        quote, author = random.choice(offline_quotes)

    messagebox.showinfo("💡 Motivation", f"{quote}\n\n— {author}")