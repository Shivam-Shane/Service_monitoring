import yaml
from logger import logging
from box.exceptions import BoxValueError
from ensure import ensure_annotations
from box import ConfigBox


@ensure_annotations
def read_yaml(path_to_yaml)-> ConfigBox: #reading yaml
    """
    Read a YAML file and return its contents as a ConfigBox.

    Args:
        path_to_yaml (str): The path to the YAML file.

    Returns:
        ConfigBox: The contents of the YAML file as a ConfigBox.

    Raises:
        ValueError: If the YAML file is empty.
        Exception: If an error occurs while reading the YAML file.
    """
    logging.info(f"Starting reading yaml file {path_to_yaml}")
    try:
        with open(path_to_yaml) as yaml_file:
            content=yaml.safe_load(yaml_file)
            logging.info(f"yaml file: {yaml_file} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e: 
        raise e   


def write_yaml(path_to_yaml,updated_data):
    """
    Write a ConfigBox to a YAML file.

    Args:
        path_to_yaml (str): The path to the YAML file.
        updated_data (ConfigBox): The updated data to write to the YAML file.
    Raises:
        Exception: If an error occurs while reading the YAML file.
    """
    logging.info(f"Starting writing yaml file {path_to_yaml}")
    try: 
        with open(path_to_yaml, "w") as yaml_file:
            yaml.dump(updated_data,yaml_file,default_flow_style=False)
            logging.info(f"yaml file: {path_to_yaml} write done successfully")    
    except Exception as e:
        raise e

def update_yaml(path_to_yaml,updates):
    """
    Update specified keys in a yaml file with new values

    Args:
        path_to_yaml (str): The path to the YAML file.
        updates (dict): The updates to be made to the YAML file in form of dict, key:value
    
    Raises:
        Exception: If an error occurs while updating the YAML file.

    """
    try:
        # Read the YAML file 
        yaml_data = read_yaml(path_to_yaml)

        # Update the yaml file with new values
        for key, value in updates.items():
            keys=key.split('.') # Split key for nested updates
            d=yaml_data
            for k in keys[:-1]:
                d=d.setdefault(k,{})# Checks if the key k exists in the current dictionary d,creates a new dictionary if not exists
            d[keys[-1]]=value
        yaml_data=yaml_data.to_dict() # saving to dictionary as read_yaml return config Box 

        # write data back to yaml file
        write_yaml(path_to_yaml,yaml_data)
        logging.info(f"yaml file: {path_to_yaml} updated successfully with {updates}")
    except Exception as e:
        raise e