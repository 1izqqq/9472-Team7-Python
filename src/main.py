import os
import json
import print_methods
from menu import Menu

file_path = 'transient_list.json'

class file_reader:
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


class Main:
    def __init__(self, file_path):
        self.file_path = file_path
        self.transients = file_reader.load_json(self.file_path)

    def run(self):
        try:
            terminal_width = os.get_terminal_size().columns
        except OSError:
            terminal_width = 110

        # Print title
        print("The Cozy Cabin".center(terminal_width))
        print("Where Every Stay Feels Like Home".center(terminal_width))

        # Show the table
        print_methods.show_transient_table(self.transients)

        menu = Menu(self.transients)
        menu.display_menu()

        self.save_data()

    def save_data(self):
        file_reader.save_json(self.transients, self.file_path)

if __name__ == "__main__":
    app = Main(file_path)
    app.run()
