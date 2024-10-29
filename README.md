# Configurationlib

A simple configuration manager for Python that allows you to easily manage nested configurations using JSON files.

## Features

- Load and save configurations from/to a JSON file.
- Create nested dictionaries dynamically.
- Retrieve configuration values easily.

## Installation

You can install the package via pip:

```bash
pip install configurationlib
```

## Usage

Here is a simple example of the usage of this module:
```python
import configurationlib

# Create an instance of the configuration manager
config = configurationlib.Instance(file="config.json") # Choose any file name you like!

# Use save() to get access to the current configuration and set values
config.save()["dic1"] = {}  # Initialize a new dictionary
config.save()["dic1"]["afewmoredic"] = {}  # Initialize a nested dictionary
config.save()["dic1"]["afewmoredic"]["key"] = "value"  # Set a value

# Retrieve values from nested dictionaries using get()
retrieved_value = config.get()["dic1"]["afewmoredic"]["key"] # Use config.get to retrieve the value
print(retrieved_value)  # Output: value

# Save changes after modifying (optional, since save is called after every modification)
config.save()
```