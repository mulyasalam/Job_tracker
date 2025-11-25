import tkinter as tk
from application import JobApplicationTracker

if __name__ == "__main__":
    root = tk.Tk()
    app = JobApplicationTracker(root)
    root.mainloop()