import pandas as pd
import json

def encode_categorical_columns(df, cat_cols, map_file):
    """
    Encode categorical columns in a Pandas dataframe and save mappings as a JSON file.

    Parameters:
    df (Pandas dataframe): the dataframe to encode
    cat_cols (list of str): the names of the categorical columns to encode
    map_file (str): the file name to save the mappings as a JSON file

    Returns:
    df (Pandas dataframe): the encoded dataframe
    """

    # Create an empty dictionary to hold the mappings
    mappings = {}

    # Loop through each categorical column
    for col in cat_cols:

        # Get the unique values in the column
        values = df[col].unique()

        # Create a dictionary to map the values to integers
        mapping = {value: i for i, value in enumerate(values)}

        # Add the mapping to the mappings dictionary
        mappings[col] = mapping

        # Replace the values in the column with the integer codes
        df[col] = df[col].map(mapping)

    # Save the mappings as a JSON file
    with open(map_file, 'w') as f:
        json.dump(mappings, f)

    return df

def decode_categorical_columns(df, map_file):
    """
    Decode categorical columns in a Pandas dataframe using mappings from a JSON file.

    Parameters:
    df (Pandas dataframe): the dataframe to decode
    map_file (str): the file name to load the mappings from

    Returns:
    df (Pandas dataframe): the decoded dataframe
    """

    # Load the mappings from the JSON file
    with open(map_file, 'r') as f:
        mappings = json.load(f)

    # Loop through each categorical column
    for col, mapping in mappings.items():

        # Invert the mapping so that the integer codes map back to the original values
        inv_mapping = {i: value for value, i in mapping.items()}

        # Replace the integer codes in the column with the original values
        df[col] = df[col].map(inv_mapping)

    return df
