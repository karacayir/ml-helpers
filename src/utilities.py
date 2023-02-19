import json


def create_class_from_config(config_file_path):

    """
    Dynamically creates a new Python class based on a JSON configuration file.

    Parameters:
       config_file_path (str): The path to the JSON configuration file.

    Returns:
       A new Python class that has been created dynamically based on the configuration file.
    """

    # Read the JSON configuration file
    with open(config_file_path, "r") as f:
        config_data = json.load(f)

    # Define a class name based on the file name
    class_name = config_file_path.split(".")[0].capitalize()

    # Define a dictionary for the class attributes
    class_attributes = {}

    # Create the class attributes from the configuration file
    for attribute_name, attribute_value in config_data.items():
        if isinstance(attribute_value, dict):
            # Recursively create a new class for the dictionary attribute
            class_attributes[attribute_name] = create_class_from_dict(attribute_value, attribute_name)
        else:
            class_attributes[attribute_name] = attribute_value

    # Create the class using the type function
    new_class = type(class_name, (object,), class_attributes)

    return new_class


def create_class_from_dict(config_dict, class_name):

    """
    Dynamically creates a new Python class based on a dictionary.

    Parameters:
        config_dict (dict): A dictionary containing the attributes of the new class.
        class_name (str): The name of the new class.

    Returns:
        A new Python class that has been created dynamically based on the provided dictionary.
    """

    # Define a class name based on the dictionary keys
    class_name = class_name.capitalize()

    # Define a dictionary for the class attributes
    class_attributes = {}

    # Create the class attributes from the dictionary keys and values
    for attribute_name, attribute_value in config_dict.items():
        if isinstance(attribute_value, dict):
            # Recursively create a new class for the nested dictionary attribute
            class_attributes[attribute_name] = create_class_from_dict(attribute_value, attribute_name)
        else:
            class_attributes[attribute_name] = attribute_value

    # Create the class using the type function
    new_class = type(class_name, (object,), class_attributes)

    return new_class


def find_indexes(items, search_list):

    """
    Finds the indexes of items in a list of search items that match a list of all items.

    Args:
        items (list): A list of items to search for.
        search_list (list): A list of all items to search within.

    Returns:
        A list of the indexes of the items in search_list that match the items. If an item is not found in search_list,
        it is not included in the output list.
    """

    return [search_list.index(col) for col in items if col in search_list]
