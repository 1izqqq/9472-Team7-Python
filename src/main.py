import os
import print_methods
import file_reader
from menu import Menu

file_path = 'transient_list.json'

def main():
    # Load JSON file
    transients = file_reader.load_json(file_path)

    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 110

    # Print title
    print("The Cozy Cabin".center(terminal_width))
    print("Where Every Stay Feels Like Home".center(terminal_width))

    # Show the table
    print_methods.show_transient_table(transients)

    # Instantiate and display the menu
    menu = Menu(transients)
    menu.display_menu()

if __name__ == "__main__":
    main()
