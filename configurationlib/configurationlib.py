import json
import os
import yaml  # Make sure to install PyYAML: pip install pyyaml

class Instance:
    def __init__(self, file, format='JSON'):
        self.file = file
        self.config = {}
        self.format_function = format()  # Normalize format to uppercase
        self.format = self.format_function.upper()
        self.load()

    def load(self):
        """Load configuration from the specified file based on its format."""
        if os.path.exists(self.file):
            with open(self.file, 'r') as f:
                if self.format == 'JSON':
                    self.config = json.load(f)
                elif self.format == 'YAML':
                    self.config = yaml.safe_load(f)
                elif self.format == 'ENV':
                    self.config = self.load_env(f)
                else:
                    raise ValueError(f"Unsupported format: {self.format}")
        else:
            self.config = {}

    def load_env(self, file):
        """Load configuration from an env file."""
        config = {}
        for line in file:
            if line.strip() and not line.startswith('#'):  # Ignore empty lines and comments
                key, value = line.strip().split('=', 1)
                config[key] = value
        return config

    def save(self):
        """Save the current configuration to the specified file based on its format."""
        with open(self.file, 'w') as f:
            if self.format == 'JSON':
                json.dump(self.config, f, indent=4)
            elif self.format == 'YAML':
                yaml.dump(self.config, f)
            elif self.format == 'ENV':
                for key, value in self.config.items():
                    f.write(f"{key}={value}\n")
            else:
                raise ValueError(f"Unsupported format: {self.format}")
        
        return self.config  # Return the current config for further manipulation

    def get(self):
        """Get the current configuration."""
        return self.config


class Format:
    @staticmethod
    def JSON():
        return "JSON"

    @staticmethod
    def YAML():
        return "YAML"

    @staticmethod
    def ENV():
        return "ENV"