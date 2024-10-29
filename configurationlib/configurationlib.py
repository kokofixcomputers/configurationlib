import json
import os

class Instance:
    def __init__(self, file):
        self.file = file
        self.config = {}
        self.load()

    def load(self):
        """Load configuration from the specified JSON file."""
        if os.path.exists(self.file):
            with open(self.file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def save(self):
        """Save the current configuration to the specified JSON file."""
        with open(self.file, 'w') as f:
            json.dump(self.config, f, indent=4)
        
        return self.config  # Return the current config for further manipulation

    def get(self):
        """Get the current configuration."""
        return self.config