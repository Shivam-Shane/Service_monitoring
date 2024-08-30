from ruamel.yaml import YAML
from logger import logging
import tempfile
import os
import shutil

def read_yaml(path_to_yaml):
    """
    Read a YAML file.

    Args:
        path_to_yaml (str): The path to the YAML file.

    Returns:
        data: The YAML data.

    Raises:
        ValueError: If the YAML file is empty.
        Exception: If an error occurs while reading the YAML file.
    """
    logging.info(f"Starting to read YAML file: {path_to_yaml}")
    try:
        yaml = YAML()
        with open(path_to_yaml, 'r') as yaml_file:
            content = yaml.load(yaml_file)
            if content is None:
                raise ValueError(f"The YAML file '{path_to_yaml}' is empty.")
            logging.info(f"YAML file '{path_to_yaml}' of type '{type(content)}' loaded successfully")
            return content
    except Exception as e:
        logging.error(f"Error reading YAML file: {e}")
        raise e

def update_yaml(path_to_yaml, updates):
    """
    Update specified keys in a YAML file with new values.

    Args:
        path_to_yaml (str): The path to the YAML file.
        updates (dict): The updates to be made to the YAML file in the form of dict, key:value pairs.
    
    Raises:
        Exception: If an error occurs while updating the YAML file.
    """
    yaml = YAML()
    
    # Create a temporary file for the update
    try:
        # Read the YAML file
        yaml_data = read_yaml(path_to_yaml)
        accept_able_yaml =read_yaml("config_acceptable_values.yaml")

        # Check each key in the dictionary and update if it is present
        for key, new_value in updates.items():
            if key in yaml_data and key in accept_able_yaml: # if keys matched in both config files
                if new_value in accept_able_yaml[key]:
                                                            # update the existing value
                    yaml_data[key] = new_value
                    logging.info(f"Updated '{key}' to '{new_value}'.")
            elif key in yaml_data and key not in accept_able_yaml:  # if only matched in config files and not in acceptable update that
                yaml_data[key] = new_value
                
                logging.info(f"Updated '{key}' to '{new_value}'.")
            else:
                logging.warning(f"Key '{key}' not found. No update performed for this key.")
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8') as temp_file:
            temp_file_name = temp_file.name
            yaml.dump(yaml_data, temp_file)
            temp_file.flush()
            os.fsync(temp_file.fileno())

        # Replace the original file with the updated temporary file
        # Use shutil.copy2() to copy the temp file to the original file path
        shutil.copy2(temp_file_name, path_to_yaml)
        os.remove(temp_file_name)  # Clean up the temporary file
        
        logging.info(f"YAML file '{path_to_yaml}' updated successfully.")
    
    except Exception as e:
        logging.error(f"Error updating YAML file: {e}")
        # Cleanup in case of error
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)
        raise e