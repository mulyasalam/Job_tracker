import tkinter as tk
from tkinter import ttk, scrolledtext

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Application Tracker")
        self.root.geometry("900x700")
        self.root.configure(bg="#f5f5f5")
        
        # Create main frame with scrollbar
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create GUI components
        self.create_widgets()
    
    def create_widgets(self):
        # Create a canvas for scrolling
        canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.scrollable_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(self.scrollable_frame, text="Job Application Tracker", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # Input fields
        ttk.Label(self.scrollable_frame, text="Company Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.company_name = ttk.Entry(self.scrollable_frame, width=40)
        self.company_name.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        ttk.Label(self.scrollable_frame, text="Job Title:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.job_title = ttk.Entry(self.scrollable_frame, width=40)
        self.job_title.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        ttk.Label(self.scrollable_frame, text="Application Link:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.job_link = ttk.Entry(self.scrollable_frame, width=40)
        self.job_link.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        ttk.Label(self.scrollable_frame, text="Status:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.status = ttk.Combobox(self.scrollable_frame, values=["Not Applied", "Applied", "Interview", "Rejected", "Offer"], width=37)
        self.status.set("Not Applied")
        self.status.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        ttk.Label(self.scrollable_frame, text="Notes:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.notes = scrolledtext.ScrolledText(self.scrollable_frame, width=30, height=4)
        self.notes.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Buttons
        self.button_frame = ttk.Frame(self.scrollable_frame)
        self.button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        self.save_button = ttk.Button(self.button_frame, text="Save Application")
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(self.button_frame, text="Clear Fields")
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        self.cancel_edit_button = ttk.Button(self.button_frame, text="Cancel Edit", state=tk.DISABLED)
        self.cancel_edit_button.pack(side=tk.LEFT, padx=5)
        
        # Status label to show edit mode
        self.status_label = ttk.Label(self.scrollable_frame, text="", foreground="blue")
        self.status_label.grid(row=7, column=0, columnspan=2, pady=5)
        
        # Separator
        separator = ttk.Separator(self.scrollable_frame, orient='horizontal')
        separator.grid(row=8, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=20)
        
        # Applications list
        ttk.Label(self.scrollable_frame, text="Saved Applications", font=("Arial", 12, "bold")).grid(row=9, column=0, columnspan=4, pady=(0, 10))
        
        # Treeview with scrollbar
        self.tree_frame = ttk.Frame(self.scrollable_frame)
        self.tree_frame.grid(row=10, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        columns = ("no", "company", "title", "status", "date")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", height=10)

        # Define headings
        self.tree.heading("no", text="No")
        self.tree.heading("company", text="Company")
        self.tree.heading("title", text="Job Title")
        self.tree.heading("status", text="Status")
        self.tree.heading("date", text="Date Added")

        # Define columns
        self.tree.column("no", width=40, anchor="center")
        self.tree.column("company", width=200)
        self.tree.column("title", width=200)
        self.tree.column("status", width=100)
        self.tree.column("date", width=120)

                # Define row colors by status
        self.tree.tag_configure("status_not_applied", background="white")
        self.tree.tag_configure("status_applied", background="white")       # applied = white
        self.tree.tag_configure("status_interview", background="lightblue")  # interview = green
        self.tree.tag_configure("status_rejected", background="lightcoral")   # rejected = red-ish
        self.tree.tag_configure("status_offer", background="green")           # offer = yellow-ish

        
        # Scrollbar for treeview
        tree_scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights for tree frame
        self.tree_frame.columnconfigure(0, weight=1)
        self.tree_frame.rowconfigure(0, weight=1)
        
        # Action buttons for applications list
        self.action_frame = ttk.Frame(self.scrollable_frame)
        self.action_frame.grid(row=11, column=0, columnspan=4, pady=10)
        
        self.view_button = ttk.Button(self.action_frame, text="View Details")
        self.view_button.pack(side=tk.LEFT, padx=5)
        
        self.edit_button = ttk.Button(self.action_frame, text="Edit Selected")
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(self.action_frame, text="Delete Selected")
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        # Pack the canvas and scrollbar in main frame
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Make the window scrollable with mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def get_form_data(self):
        return {
            "company": self.company_name.get().strip(),
            "title": self.job_title.get().strip(),
            "link": self.job_link.get().strip(),
            "status": self.status.get(),
            "notes": self.notes.get("1.0", tk.END).strip()
        }
    
    def set_form_data(self, data):
        self.clear_fields()
        self.company_name.insert(0, data["company"])
        self.job_title.insert(0, data["title"])
        self.job_link.insert(0, data["link"])
        self.status.set(data["status"])
        self.notes.insert("1.0", data["notes"])
    
    def clear_fields(self):
        self.company_name.delete(0, tk.END)
        self.job_title.delete(0, tk.END)
        self.job_link.delete(0, tk.END)
        self.status.set("Not Applied")
        self.notes.delete("1.0", tk.END)
    
    def set_edit_mode(self, is_editing):
        if is_editing:
            self.save_button.config(text="Update Application")
            self.cancel_edit_button.config(state=tk.NORMAL)
            self.status_label.config(text="Edit Mode: Editing existing application")
        else:
            self.save_button.config(text="Save Application")
            self.cancel_edit_button.config(state=tk.DISABLED)
            self.status_label.config(text="")
    
    def load_applications_list(self, applications):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add applications to treeview
        for idx, app in enumerate(applications):
            row_no = idx + 1  # 1, 2, 3, ...

            display_date = app.get("last_updated", app["date_added"])
            status = app.get("status", "Not Applied")

            # Pick a tag for the status color
            status_lower = status.lower()
            if status_lower == "applied":
                status_tag = "status_applied"
            elif status_lower == "interview":
                status_tag = "status_interview"
            elif status_lower == "rejected":
                status_tag = "status_rejected"
            else:
                status_tag = "status_not_applied"

            # tags = (index_tag, color_tag)
            self.tree.insert(
                "",
                tk.END,
                values=(
                    row_no,
                    app["company"],
                    app["title"],
                    status,
                    display_date
                ),
                tags=(str(idx), status_tag)
            )


    
    def get_selected_application_index(self):
        selected = self.tree.selection()
        if not selected:
            return -1
        item = self.tree.item(selected[0])
        return int(item["tags"][0])  # first tag = index


