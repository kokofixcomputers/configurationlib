# Configurationlib

A simple configuration manager for Python that allows you to easily manage nested configurations using JSON files.

## Features

- Load and save configurations from/to a JSON, YAML or .env file.
- Create nested dictionaries dynamically.
- Retrieve configuration values easily.

## Installation

You can install the package via pip:

```bash
pip install configurationlib
```

## Note
If the file specified does not exist, it will be created.

## Usage


> [!WARNING]
> Please do note, if you specify the wrong file with the wrong format, it may load incorrectly or may break your file.


Here is a simple example of the usage of this module:
```python
import configurationlib

# Create an instance of the configuration manager
config = configurationlib.Instance(file="config.json") # Choose any file name you like! The file will be created if it does not exist.

# Use save() to get access to the current configuration and set values
config.save()["dic1"] = {}  # Initialize a new dictionary
config.save()["dic1"]["afewmoredic"] = {}  # Initialize a nested dictionary
config.save()["dic1"]["afewmoredic"]["key"] = "value"  # Set a value
config.save()['weird'] = True

# Retrieve values from nested dictionaries using get()
retrieved_value = config.get()["dic1"]["afewmoredic"]["key"] # Use config.get to retrieve the value
print(retrieved_value)  # Output: value

# Save changes after modifying (optional, since save is called after every modification)
config.save()
```
### Changing formats
If you want, You can change the format of the saved file (YAML, JSON, dotENV) the default already is JSON so if you want json, you don't need to do anything.
Here is how you can change it to YAML:
```python
import configurationlib

# Create an instance of the configuration manager
config = configurationlib.Instance(file="config.json", format=configurationlib.Format.YAML) # Use Yaml. Change this to ENV to use env

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
The only line that changes is `config = configurationlib.Instance(file="config.json", format=configurationlib.Format.YAML` nothing else changes. It will automatically save the data into the data you'd like! If you remove format argument, it will default to `JSON`.

### Hot Reloading
> [!NOTE]
> Hot reloading is disabled by default
If you want to enable hot reloading, Use this:
```python
config = configurationlib.Instance(file="config.json", format=configurationlib.Format.YAML, hot_reloading=True)
```
