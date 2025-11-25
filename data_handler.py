import json
import os
from datetime import datetime

class DataHandler:
    def __init__(self, data_file="job_applications.json"):
        self.data_file = data_file
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_data(self, applications):
        with open(self.data_file, 'w') as f:
            json.dump(applications, f, indent=2)
    
    def get_current_datetime(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M")