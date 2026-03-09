import json
import os
from pathlib import Path

class JSONLoader:
    """
    Utility to load test data from JSON files located in the application's data/json folder.
    """
    
    @staticmethod
    def load_test_data(app_path: str, filename: str) -> dict:
        """
        Loads a JSON file given the application path and filename.
        
        Args:
            app_path (str): The absolute path to the application directory.
            filename (str): The name of the JSON file (e.g., 'login_data.json').
            
        Returns:
            dict: The parsed JSON content.
        """
        # Ensure filename has .json extension
        if not filename.endswith(".json"):
            filename += ".json"
            
        full_path = os.path.join(app_path, "data", "json", filename)
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"JSON data file not found at: {full_path}")
            
        with open(full_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        return data

    @staticmethod
    def get_test_case_data(json_content: dict) -> dict:
        """
        Extracts the 'data' object from the structured JSON content.
        
        Args:
            json_content (dict): The full content of a data JSON.
            
        Returns:
            dict: The 'data' object.
        """
        tests = json_content.get("tests", {})
        return tests.get("data", {})
