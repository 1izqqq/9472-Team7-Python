import json

class FileReader:
    @staticmethod
    def load_json(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            FileReader._handle_error(f"The file '{file_path}' was not found.")
        except json.JSONDecodeError:
            FileReader._handle_error(f"The file '{file_path}' is not a valid JSON.")
        return []

    @staticmethod
    def save_json(data, file_path):
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Data successfully saved to '{file_path}'")
        except Exception as e:
            FileReader._handle_error(f"Error saving to '{file_path}': {e}")

    @staticmethod
    def _handle_error(message):
        print(f"Error: {message}")
