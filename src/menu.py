import sort_filter
import print_methods
from reservation import show_available_dates, reserve_dates
from reservation import enter_choice

class Menu:
    def __init__(self, transients):
        self.transients = transients

    def display_menu(self):
        while True:
            print("\nMain Menu")
            print("1. Select transient to book")
            print("2. Sort transient list")
            print("3. Filter transient list")
            print("4. Exit Cozy Cabin")
            choice = enter_choice(1,4, "Enter a number from the menu: ")

            if choice == 1:
                self.select_transient()
            elif choice == 2:
                self.sort_menu()
            elif choice == 3:
                self.filter_menu()
            elif choice == 4:
                exit(0)

    def select_transient(self):
        print_methods.show_transient_table(self.transients)
        user_input = input("Please input transient house's ID: ").strip()
        try:
            option = int(user_input)
            selected_transient = next((t for t in self.transients if t['id'] == option), None)
            if selected_transient:
                available_dates = show_available_dates(selected_transient)
                if available_dates:
                    reserve_dates(selected_transient, available_dates, self.transients)
            else:
                print("Invalid ID. Please enter a valid transient house ID!")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def sort_menu(self):
        while True:
            print("\nSort")
            print("1. Sort by price in ascending order")
            print("2. Sort by price in descending order")
            print("3. Sort by ID")
            print("4. Go back to Main Menu")

            choice_sort = enter_choice(1,4,"Enter a number from the menu: ")

            if choice_sort == 1:
                sorted_transient = sort_filter.sort_transients_price(self.transients, "asc")
                print_methods.show_transient_table(sorted_transient)
            elif choice_sort == 2:
                sorted_transient = sort_filter.sort_transients_price(self.transients, "desc")
                print_methods.show_transient_table(sorted_transient)
            elif choice_sort == 3:
                print_methods.show_transient_table(self.transients)
            elif choice_sort == 4:
                break

    def filter_menu(self):
        while True:
            print("\nFilter")
            print("1. Filter by transient name")
            print("2. Filter by address")
            print("3. Go back to Main Menu")

            choice_filter = enter_choice(1,3,"Enter a number from the menu: ")

            if choice_filter in [1, 2]:
                filter_query = input("Enter your filter query: ").strip()
                if filter_query:
                    filtered_transients = sort_filter.filter_transients(self.transients, choice_filter, filter_query)
                    if filtered_transients:
                        print_methods.show_transient_table(filtered_transients)
                    else:
                        print(f"\nNo transients found matching the query: {filter_query}")
                else:
                    print("Filter query cannot be empty.")
            elif choice_filter == 3:
                break
