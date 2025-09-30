import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime

class JobApplicationTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Application Tracker")
        self.root.geometry("900x700")  # Increased height to ensure all elements fit
        self.root.configure(bg="#f5f5f5")
        
        # Data file
        self.data_file = "job_applications.json"
        
        # Track if we're in edit mode and which item we're editing
        self.edit_mode = False
        self.editing_index = -1
        
        # Initialize data
        self.applications = self.load_data()
        
        # Create GUI
        self.create_gui()
        
        # Load existing applications
        self.load_applications_list()
    
    def create_gui(self):
        # Main frame with scrollbar
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add a canvas for scrolling
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
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
        button_frame = ttk.Frame(self.scrollable_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        self.save_button = ttk.Button(button_frame, text="Save Application", command=self.save_application)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear Fields", command=self.clear_fields).pack(side=tk.LEFT, padx=5)
        
        self.cancel_edit_button = ttk.Button(button_frame, text="Cancel Edit", command=self.cancel_edit, state=tk.DISABLED)
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
        tree_frame = ttk.Frame(self.scrollable_frame)
        tree_frame.grid(row=10, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        columns = ("company", "title", "status", "date")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        
        # Define headings
        self.tree.heading("company", text="Company")
        self.tree.heading("title", text="Job Title")
        self.tree.heading("status", text="Status")
        self.tree.heading("date", text="Date Added")
        
        # Define columns
        self.tree.column("company", width=200)
        self.tree.column("title", width=200)
        self.tree.column("status", width=100)
        self.tree.column("date", width=120)
        
        # Scrollbar for treeview
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights for tree frame
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Action buttons for applications list - FIXED TO BE VISIBLE
        action_frame = ttk.Frame(self.scrollable_frame)
        action_frame.grid(row=11, column=0, columnspan=4, pady=10)
        
        ttk.Button(action_frame, text="View Details", command=self.view_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Edit Selected", command=self.edit_application).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Delete Selected", command=self.delete_application).pack(side=tk.LEFT, padx=5)
        
        # Pack the canvas and scrollbar in main frame
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind tree selection
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        
        # Make the window scrollable with mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.applications, f, indent=2)
    
    def save_application(self):
        company = self.company_name.get().strip()
        title = self.job_title.get().strip()
        link = self.job_link.get().strip()
        status = self.status.get()
        notes = self.notes.get("1.0", tk.END).strip()
        
        if not company or not title:
            messagebox.showerror("Error", "Company name and job title are required!")
            return
        
        application = {
            "company": company,
            "title": title,
            "link": link,
            "status": status,
            "notes": notes,
            "date_added": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        if self.edit_mode:
            # Update existing application
            self.applications[self.editing_index] = application
            message = "Application updated successfully!"
        else:
            # Add new application
            self.applications.append(application)
            message = "Application saved successfully!"
        
        self.save_data()
        self.load_applications_list()
        self.clear_fields()
        
        if self.edit_mode:
            self.cancel_edit()  # Exit edit mode
        
        messagebox.showinfo("Success", message)
    
    def clear_fields(self):
        self.company_name.delete(0, tk.END)
        self.job_title.delete(0, tk.END)
        self.job_link.delete(0, tk.END)
        self.status.set("Not Applied")
        self.notes.delete("1.0", tk.END)
    
    def cancel_edit(self):
        self.edit_mode = False
        self.editing_index = -1
        self.clear_fields()
        self.save_button.config(text="Save Application")
        self.cancel_edit_button.config(state=tk.DISABLED)
        self.status_label.config(text="")
    
    def enter_edit_mode(self, index):
        self.edit_mode = True
        self.editing_index = index
        self.save_button.config(text="Update Application")
        self.cancel_edit_button.config(state=tk.NORMAL)
        self.status_label.config(text="Edit Mode: Editing existing application")
    
    def load_applications_list(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add applications to treeview
        for i, app in enumerate(self.applications):
            display_date = app.get("last_updated", app["date_added"])
            self.tree.insert("", tk.END, values=(
                app["company"], 
                app["title"], 
                app["status"], 
                display_date
            ), tags=(i,))
    
    def view_details(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an application to view.")
            return
        
        item = self.tree.item(selected[0])
        index = item["tags"][0]
        
        app = self.applications[index]
        details = f"Company: {app['company']}\n"
        details += f"Job Title: {app['title']}\n"
        details += f"Link: {app['link']}\n"
        details += f"Status: {app['status']}\n"
        details += f"Date Added: {app['date_added']}\n"
        if 'last_updated' in app:
            details += f"Last Updated: {app['last_updated']}\n"
        details += f"Notes:\n{app['notes']}"
        
        messagebox.showinfo("Application Details", details)
    
    def edit_application(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an application to edit.")
            return
        
        item = self.tree.item(selected[0])
        index = item["tags"][0]
        
        # Fill the fields with existing data
        self.clear_fields()
        app = self.applications[index]
        
        self.company_name.insert(0, app["company"])
        self.job_title.insert(0, app["title"])
        self.job_link.insert(0, app["link"])
        self.status.set(app["status"])
        self.notes.insert("1.0", app["notes"])
        
        # Enter edit mode
        self.enter_edit_mode(index)
    
    def delete_application(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an application to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this application?"):
            item = self.tree.item(selected[0])
            index = item["tags"][0]
            
            # Remove the application
            self.applications.pop(index)
            self.save_data()
            self.load_applications_list()
            
            # If we were editing this item, cancel edit mode
            if self.edit_mode and self.editing_index == index:
                self.cancel_edit()
    
    def on_tree_double_click(self, event):
        self.view_details()

if __name__ == "__main__":
    root = tk.Tk()
    app = JobApplicationTracker(root)
    root.mainloop()