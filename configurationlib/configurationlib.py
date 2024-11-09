import json
import os
import yaml  # Make sure to install PyYAML: pip install pyyaml
import configparser  # For INI files

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
                elif self.format == 'PYTHON':
                    self.config = self.load_python(self.file)
                elif self.format == 'INI':
                    self.config = self.load_ini(f)
                else:
                    raise ValueError(f"Unsupported format: {self.format}")
        else:
            self.config = {}

    def load_python(self, file):
        """Load configuration from a Python script."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        config_vars = {}
        for var in dir(module):
            if not var.startswith('__') and var.isidentifier():
                config_vars[var] = getattr(module, var)

        return config_vars
    
    def load_ini(self, file):
        """Load configuration from an INI file."""
        config = configparser.ConfigParser()
        config.read_file(file)
        return {section: dict(config.items(section)) for section in config.sections()}

    def load_env(self, file):
        """Load configuration from an env file."""
        config = {}
        for line in file:
            if line.strip() and not line.startswith('#'):
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
            elif self.format == 'PYTHON':
                for key, value in self.config.items():
                    f.write(f"{key} = {repr(value)}\n")  # Write each key-value pair as a separate variable
            elif self.format == 'INI':
                config = configparser.ConfigParser()
                
                for section, values in self.config.items():
                    config[section] = {}
                    if isinstance(values, dict):
                        for key, value in values.items():
                            config[section][key] = str(value)  # Convert all values to string
                    else:
                        config[section][section] = str(values)

                config.write(f)
            else:
                raise ValueError(f"Unsupported format: {self.format}")

        return self.config  # Ensure it returns the current config for further manipulation

    def get(self):
        """Get the current configuration."""
        return self.config

    def __setitem__(self, key, value):
        """Allow setting values directly using dictionary-like syntax."""
        
        keys = key.split('.')
        
        current_level = self.config
        
        for k in keys[:-1]:
            if k not in current_level or not isinstance(current_level[k], dict):
                current_level[k] = {}
            current_level = current_level[k]

        current_level[keys[-1]] = value
        
        return self.save()  # Ensure it saves and returns updated config

    def __getitem__(self, key):
        """Allow getting values directly using dictionary-like syntax."""
        
        keys = key.split('.')
        
        current_level = self.config
        
        for k in keys:
            current_level = current_level.get(k)  
        
        return current_level

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
    
    @staticmethod
    def PYTHON():
        return "PYTHON"
    
    @staticmethod
    def INI():
        return "INI"
