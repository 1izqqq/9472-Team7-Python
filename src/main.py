import os
import print_methods
from menu import Menu
from file_reader import FileReader

file_path = '../transient_list.json'

class Main:
    def __init__(self, file_path):
        self.file_path = file_path
        self.transients = FileReader.load_json(self.file_path)

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
        FileReader.save_json(self.transients, self.file_path)

if __name__ == "__main__":
    app = Main(file_path)
    app.run()
