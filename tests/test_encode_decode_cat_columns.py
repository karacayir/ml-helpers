import json
import os
import unittest
from tempfile import NamedTemporaryFile

import pandas as pd

from src.data_manipulation import decode_categorical_columns, encode_categorical_columns


class TestEncodeDecodeCategoricalColumns(unittest.TestCase):
    def setUp(self):
        # Create a sample dataframe with categorical columns
        self.df = pd.DataFrame(
            {
                "id": [1, 2, 3, 4, 5],
                "color": ["red", "green", "red", "blue", "green"],
                "size": ["S", "M", "L", "XL", "M"],
            }
        )

    def test_encode_categorical_columns(self):
        # Create a temporary file for the mappings
        with NamedTemporaryFile(mode="w", delete=False) as map_file:
            map_file_name = map_file.name

        # Encode the categorical columns and save the mappings to the temporary file
        df_encoded = encode_categorical_columns(self.df, ["color", "size"], map_file_name)

        # Verify that the encoding is correct
        self.assertEqual(df_encoded["color"].tolist(), [0, 1, 0, 2, 1])
        self.assertEqual(df_encoded["size"].tolist(), [0, 1, 2, 3, 1])

        # Verify that the mappings file exists and is not empty
        self.assertTrue(os.path.isfile(map_file_name))
        self.assertTrue(os.path.getsize(map_file_name) > 0)

        # Load the mappings from the file and verify that they are correct
        with open(map_file_name, "r") as f:
            mappings = json.load(f)
        self.assertEqual(mappings["color"], {"red": 0, "green": 1, "blue": 2})
        self.assertEqual(mappings["size"], {"S": 0, "M": 1, "L": 2, "XL": 3})

        # Clean up the temporary file
        os.remove(map_file_name)

    def test_decode_categorical_columns(self):
        # Create a temporary file for the mappings
        with NamedTemporaryFile(mode="w", delete=False) as map_file:
            map_file_name = map_file.name

        # Encode the categorical columns and save the mappings to the temporary file
        df_encoded = encode_categorical_columns(self.df, ["color", "size"], map_file_name)

        # Decode the categorical columns using the mappings from the temporary file
        df_decoded = decode_categorical_columns(df_encoded, map_file_name)

        # Verify that the decoding is correct
        self.assertTrue(self.df.equals(df_decoded))

        # Clean up the temporary file
        os.remove(map_file_name)


if __name__ == "__main__":
    unittest.main()
