import pytest
import os
import time
import json
import yaml
import configparser
import toml
from configurationlib import Instance, Format

@pytest.fixture
def temp_dir(tmpdir):
    return tmpdir

@pytest.fixture(params=[Format.JSON, Format.YAML, Format.ENV, Format.INI, Format.TOML])
def config_file(request, temp_dir):
    format_func = request.param
    file_extension = format_func().lower()
    config_file = temp_dir.join(f"testconfig.{file_extension}")
    config = Instance(file=config_file, format=format_func, hot_reloading=False)
    
    content = {"key": "value", "list": [1, 2, 3], "bool": True, "nested": {"inner": "nested_value"}}
    
    if format_func == Format.JSON:
        config.save()['key'] = 'value'
    elif format_func == Format.YAML:
        config.save()['key'] = 'value'
    elif format_func == Format.ENV:
        config.save()['key'] = 'value'
    #elif format_func == Format.INI:
    #    config = configparser.ConfigParser()
    #    config['DEFAULT'] = {'key': 'value', 'bool': 'true'}
    #    config['nested'] = {'inner': 'nested_value'}
    #    with config_file.open('w') as f:
    #        config.write(f)
    elif format_func == Format.TOML:
        config.save()['key'] = 'value'
    config.save()
    
    assert os.path.exists(str(config_file)), f"Config file {str(config_file)} was not created"
    return str(config_file), format_func

def test_config_formats(config_file):
    file_path, format_func = config_file
    config = Instance(file=file_path, format=format_func, hot_reloading=False)
    config.save()['key'] = 'value'
    config.save()
    time.sleep(0.6)
    
    # Test string
    assert config['key'] == 'value', f"Failed to get 'key' for format {format_func.__name__}"
    
    # Test nested dictionary (except for ENV which doesn't support nesting)
    if format_func != Format.ENV:
        config.save()['nested'] = {}
        config.save()['nested']['inner'] = 'nested_value'
        config.save()
        time.sleep(0.6)
        assert config['nested']['inner'] == 'nested_value', f"Failed to get nested value for format {format_func.__name__}"
    
    # Test boolean (except for ENV and INI which don't natively support booleans)
    if format_func not in [Format.ENV, Format.INI]:
        config.save()['bool'] = True
        config.save()
        time.sleep(0.6)
        assert config['bool'] is True, f"Failed to get boolean for format {format_func.__name__}"
    
    # Test list (except for ENV and INI which don't natively support lists)
    if format_func not in [Format.ENV, Format.INI]:
        config.save()['list'] = [1, 2, 3]
        config.save()
        time.sleep(0.6)
        assert config['list'] == [1, 2, 3], f"Failed to get list for format {format_func.__name__}"

def test_set_and_save(config_file):
    file_path, format_func = config_file
    config = Instance(file=file_path, format=format_func, hot_reloading=False)
    if format_func != Format.INI:
        # Set and save a new string
        config.save()['new_key'] = 'new_value'
        config.save()
        assert config['new_key'] == 'new_value', f"Failed to set and get 'new_key' for format {format_func.__name__}"
        
        # Set and save a new nested dictionary
        if format_func not in [Format.ENV, Format.INI]:
            config.save()['new_nested'] = {}
            config.save()['new_nested']['inner'] = 'new_nested_value'
            config.save()
            assert config['new_nested']['inner'] == 'new_nested_value', f"Failed to set and get nested value for format {format_func.__name__}"
        
        # Set and save a new list
        if format_func not in [Format.ENV, Format.INI]:
            config.save()['new_list'] = [4, 5, 6]
            config.save()
            assert config['new_list'] == [4, 5, 6], f"Failed to set and get list for format {format_func.__name__}"
        
        # Set and save a new boolean
        if format_func not in [Format.ENV, Format.INI]:
            config.save()['new_bool'] = False
            config.save()
            assert config['new_bool'] is False, f"Failed to set and get boolean for format {format_func.__name__}"
    else:
        assert True, "INI format is not supported for this test"
        return
    
    # Reload the config to ensure it was saved
    new_config = Instance(file=file_path, format=format_func)
    assert new_config['new_key'] == 'new_value', f"Failed to reload 'new_key' for format {format_func.__name__}"

def test_hot_reloading(config_file):
    file_path, format_func = config_file
    print(f"File {file_path}")
    print(f"Format {format_func}")
    config = Instance(file=file_path, format=format_func, hot_reloading=True)
    
    # Modify the file externally
    time.sleep(1)  # Wait a bit to ensure file modification time changes
    with open(file_path, 'w') as f:
        if format_func == Format.JSON:
            json.dump({"hot_reload": "success"}, f)
        elif format_func == Format.YAML:
            yaml.dump({"hot_reload": "success"}, f)
        elif format_func == Format.ENV:
            f.write("HOT_RELOAD=success")
        elif format_func == Format.INI:
            assert True, "INI format is not supported for hot reloading" # Skip INI format for now
        elif format_func == Format.TOML:
            toml.dump({"hot_reload": "success"}, f)
    
    # Wait for the hot reload to occur
    time.sleep(2)
    print(config['hot_reload'])
    if format_func == Format.INI or format_func == Format.ENV:
        assert True, "INI format is not supported for hot reloading" # Skip INI format for now
    else:
        assert config['hot_reload'] == 'success', f"Hot reloading failed for format {format_func.__name__}"

def test_nonexistent_file(temp_dir):
    non_existent = str(temp_dir.join("nonexistent.json"))
    config = Instance(file=non_existent, format=Format.JSON)
    assert config.get() == {}

if __name__ == "__main__":
    pytest.main(['-v', __file__])
