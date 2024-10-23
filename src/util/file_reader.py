import json

class FileReader:
    @staticmethod
    def load_json(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except json.JSONDecodeError:
            print(f"Error: The file '{file_path}' is not a valid JSON.")
        return []

    @staticmethod
    def save_json(transients, file_path):
        try:
            with open(file_path, 'w') as file:
                json.dump(transients, file, indent=4)
            print(f"Data successfully saved to '{file_path}'")
        except Exception as e:
            print(f"Error saving to '{file_path}': {e}")
            raise