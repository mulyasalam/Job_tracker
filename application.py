import tkinter as tk
from tkinter import messagebox
from data_handler import DataHandler

class JobApplicationTracker:
    def __init__(self, root):
        self.root = root
        self.data_handler = DataHandler()
        self.applications = self.data_handler.load_data()
        
        # Import GUI here to avoid circular imports
        from gui import GUI
        self.gui = GUI(root)
        
        # Set up event handlers
        self.setup_handlers()
        
        # Load existing applications
        self.gui.load_applications_list(self.applications)
        
        # Track edit mode
        self.edit_mode = False
        self.editing_index = -1
    
    def setup_handlers(self):
        # Connect buttons to methods
        self.gui.save_button.config(command=self.save_application)
        self.gui.clear_button.config(command=self.clear_fields)
        self.gui.cancel_edit_button.config(command=self.cancel_edit)
        self.gui.view_button.config(command=self.view_details)
        self.gui.edit_button.config(command=self.edit_application)
        self.gui.delete_button.config(command=self.delete_application)
        
        # Bind tree selection
        self.gui.tree.bind("<Double-1>", self.on_tree_double_click)
    
    def save_application(self):
        form_data = self.gui.get_form_data()
        company = form_data["company"]
        title = form_data["title"]
        link = form_data["link"]
        status = form_data["status"]
        notes = form_data["notes"]
        
        if not company or not title:
            messagebox.showerror("Error", "Company name and job title are required!")
            return
        
        application = {
            "company": company,
            "title": title,
            "link": link,
            "status": status,
            "notes": notes,
            "date_added": self.data_handler.get_current_datetime(),
            "last_updated": self.data_handler.get_current_datetime()
        }
        
        if self.edit_mode:
            # Update existing application
            self.applications[self.editing_index] = application
            message = "Application updated successfully!"
        else:
            # Add new application
            self.applications.append(application)
            message = "Application saved successfully!"
        
        self.data_handler.save_data(self.applications)
        self.gui.load_applications_list(self.applications)
        self.clear_fields()
        
        if self.edit_mode:
            self.cancel_edit()
        
        messagebox.showinfo("Success", message)
    
    def clear_fields(self):
        self.gui.clear_fields()
    
    def cancel_edit(self):
        self.edit_mode = False
        self.editing_index = -1
        self.gui.set_edit_mode(False)
        self.clear_fields()
    
    def view_details(self):
        index = self.gui.get_selected_application_index()
        if index == -1:
            messagebox.showwarning("Warning", "Please select an application to view.")
            return
        
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
        index = self.gui.get_selected_application_index()
        if index == -1:
            messagebox.showwarning("Warning", "Please select an application to edit.")
            return
        
        # Fill the fields with existing data
        app = self.applications[index]
        self.gui.set_form_data(app)
        
        # Enter edit mode
        self.edit_mode = True
        self.editing_index = index
        self.gui.set_edit_mode(True)
    
    def delete_application(self):
        index = self.gui.get_selected_application_index()
        if index == -1:
            messagebox.showwarning("Warning", "Please select an application to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this application?"):
            # Remove the application
            self.applications.pop(index)
            self.data_handler.save_data(self.applications)
            self.gui.load_applications_list(self.applications)
            
            # If we were editing this item, cancel edit mode
            if self.edit_mode and self.editing_index == index:
                self.cancel_edit()
    
    def on_tree_double_click(self, event):
        self.view_details()