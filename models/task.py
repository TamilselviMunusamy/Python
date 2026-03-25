class Task:
    def __init__(self, text, time, priority="Medium", category="General", completed=False, notes=""):
        self.text = text
        self.time = time
        self.priority = priority
        self.category = category
        self.completed = completed
        self.notes = notes

    def to_dict(self):
        return self.__dict__