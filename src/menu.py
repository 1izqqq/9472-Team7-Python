import sort_filter
import print_methods
from reservation import show_available_dates, reserve_dates

class Menu:
    def __init__(self, transients):
        self.transients = transients

    def display_menu(self):
        menu_actions = {
            1: self.select_transient,
            2: self.sort_menu,
            3: self.filter_menu,
            4: self.exit_program
        }

        while True:
            self.print_main_menu()
            choice = self.enter_choice(1, 4, "Enter a number from the menu: ")
            action = menu_actions.get(choice)
            if action:
                action()
            else:
                print("Invalid choice. Please try again.")

    def enter_choice(self, min_choice, max_choice, prompt):
        from reservation import enter_choice  # Import moved inside the method
        return enter_choice(min_choice, max_choice, prompt)

    def print_main_menu(self):
        print("\nMain Menu")
        print("1. Select transient to book")
        print("2. Sort transient list")
        print("3. Filter transient list")
        print("4. Exit Cozy Cabin")

    def exit_program(self):
        exit(0)

    def select_transient(self):
        print_methods.show_transient_table(self.transients)
        user_input = input("Please input transient house's ID: ").strip()
        selected_transient = self.get_selected_transient(user_input)
        if selected_transient:
            available_dates = show_available_dates(selected_transient)
            if available_dates:
                reserve_dates(selected_transient, available_dates, self.transients)

    def get_selected_transient(self, user_input):
        try:
            option = int(user_input)
            return next((t for t in self.transients if t['id'] == option), None)
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None

    def sort_menu(self):
        sort_actions = {
            1: lambda: self.sort_transients("asc"),
            2: lambda: self.sort_transients("desc"),
            3: self.show_unsorted_transients,
            4: self.back_to_main_menu
        }

        while True:
            self.print_sort_menu()
            choice_sort = self.enter_choice(1, 4, "Enter a number from the menu: ")
            action = sort_actions.get(choice_sort)
            if action:
                action()
            else:
                print("Invalid choice. Please try again.")

    def print_sort_menu(self):
        print("\nSort")
        print("1. Sort by price in ascending order")
        print("2. Sort by price in descending order")
        print("3. Sort by ID")
        print("4. Go back to Main Menu")

    def sort_transients(self, order):
        sorted_transient = sort_filter.sort_transients_price(self.transients, order)
        print_methods.show_transient_table(sorted_transient)

    def show_unsorted_transients(self):
        print_methods.show_transient_table(self.transients)

    def back_to_main_menu(self):
        return

    def filter_menu(self):
        filter_actions = {
            1: lambda: self.apply_filter(1),
            2: lambda: self.apply_filter(2),
            3: self.back_to_main_menu
        }

        while True:
            self.print_filter_menu()
            choice_filter = self.enter_choice(1, 3, "Enter a number from the menu: ")
            action = filter_actions.get(choice_filter)
            if action:
                action()
            else:
                print("Invalid choice. Please try again.")

    def print_filter_menu(self):
        print("\nFilter")
        print("1. Filter by transient name")
        print("2. Filter by address")
        print("3. Go back to Main Menu")

    def apply_filter(self, choice_filter):
        filter_query = input("Enter your filter query: ").strip()
        if filter_query:
            filtered_transients = sort_filter.filter_transients(self.transients, choice_filter, filter_query)
            if filtered_transients:
                print_methods.show_transient_table(filtered_transients)
            else:
                print(f"\nNo transients found matching the query: {filter_query}")
        else:
            print("Filter query cannot be empty.")
