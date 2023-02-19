import json
import os
import unittest

from src.utilities import create_class_from_config, create_class_from_dict, find_indexes


class TestUtils(unittest.TestCase):
    def test_create_class_from_config(self):
        # Define a test configuration file
        config = {
            "attribute1": "value1",
            "attribute2": {"nested_attribute1": "nested_value1", "nested_attribute2": "nested_value2"},
        }
        config_file_path = "test_config.json"
        with open(config_file_path, "w") as f:
            json.dump(config, f)

        # Test creating a class from the test configuration file
        TestClass = create_class_from_config(config_file_path)
        obj = TestClass()

        # Check that the class attributes were set correctly
        self.assertEqual(obj.attribute1, "value1")
        self.assertEqual(obj.attribute2.nested_attribute1, "nested_value1")
        self.assertEqual(obj.attribute2.nested_attribute2, "nested_value2")

        os.remove("test_config.json")

    def test_create_class_from_dict(self):
        # Define a test dictionary
        config_dict = {
            "attribute1": "value1",
            "attribute2": {"nested_attribute1": "nested_value1", "nested_attribute2": "nested_value2"},
        }

        # Test creating a class from the test dictionary
        TestClass = create_class_from_dict(config_dict, "TestClass")
        obj = TestClass()

        # Check that the class attributes were set correctly
        self.assertEqual(obj.attribute1, "value1")
        self.assertEqual(obj.attribute2.nested_attribute1, "nested_value1")
        self.assertEqual(obj.attribute2.nested_attribute2, "nested_value2")

    def test_find_indexes(self):
        # Define test lists
        items = ["b", "d"]
        search_list = ["a", "b", "c", "d", "e"]

        # Test finding the indexes of the items in the search list
        indexes = find_indexes(items, search_list)

        # Check that the indexes were found correctly
        self.assertEqual(indexes, [1, 3])


if __name__ == "__main__":
    unittest.main()
