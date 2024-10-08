import os
import json
import re

from prettytable import PrettyTable
from datetime import datetime, timedelta

# File path where the JSON file is saved
file_path = 'transient_list.json'

# Load JSON file
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to display the transient table
def show_transient_table(transients):
    main_table = PrettyTable()
    main_table.field_names = ["ID", "Name", "Address", "Price/Head", "Contact"]

    for transient in transients:
        main_table.add_row(
            [transient["id"], transient["name"], transient["location"],
             f"₱{transient['price_per_head']}", transient["contact"]])

    print(main_table)

def sort_transients(transients, sort_choice):
    transients_sorted_asc = sorted(transients, key=lambda x: x["price_per_head"])
    transients_sorted_desc = sorted(transients, key=lambda x: x["price_per_head"], reverse=True)
    if sort_choice == 1:
        return transients_sorted_asc
    elif sort_choice == 2:
        return transients_sorted_desc
    else:
        return transients

def filter_transients(transients, filter_choice, filter_query):
    if filter_choice == 1:
        return [t for t in transients if filter_query.lower() in t["name"].lower()]
    elif filter_choice == 2:
        return [t for t in transients if filter_query.lower() in t["location"].lower()]
    return transients

def show_available_dates(transient):
    print(f"Name: {transient['name']}")
    print(f"Description: {transient['description']}")
    print(f"Please check available dates for {transient['name']}:")
    print()

    available_dates = [] # List holding available dates
    available_dates_table = PrettyTable()
    available_dates_table.field_names = ["ID", "Dates", "Status"]

    index = 0

    for date, details in transient['availability'].items():
        status = details['status'].upper()
        # Remove dates with "RESERVED" status
        if status != "RESERVED":
            index += 1
            available_dates_table.add_row([index, date, status])
            available_dates.append(date)

    # Notify user if there are no available dates in a transient
    if len(available_dates) == 0:
        print("This transient has no available dates.")
        return None

    print(available_dates_table)
    return set(available_dates)

def reserve_dates(transient, available_dates, transients):
    available_dates_list = list(available_dates)
    available_dates_list.sort()
    while True:
        ans_input = input("Would you like to reserve? (y/n) ").strip().lower()
        if ans_input in ["y", "yes"]:
            try:
                print()
                print("Reservation Form")
                while True:
                    client_name = input("Enter client name: ").strip()
                    # Client name must not contain any integer
                    if not re.match("^[A-Za-z\\s\\-]+$", client_name):
                        print("Invalid name! Client name should not contain numbers or special characters. Please try again.")
                    else:
                        break
                date_from = input_reserve_date("Enter ID to select reservation start date: ", available_dates_list)
                date_to = input_reserve_date("Enter ID to select reservation end date: ", available_dates_list)
                while True:
                    number_of_people = (input("Enter number of people: ").strip())
                    # Validates if input is integer
                    if number_of_people.isdigit():
                        number_of_people = int(number_of_people)
                        if number_of_people > 0:
                            break
                        else:
                            print("Number of people must be greater than 0. Please try again.")
                    else:
                        print("Please enter a valid integer for number of people. Please try again.")

                # Validate date format
                try:
                    start_date = datetime.strptime(date_from, '%Y-%m-%d')
                    end_date = datetime.strptime(date_to, '%Y-%m-%d')
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
                    continue

                # Validate date range
                if start_date > end_date:
                    print("Error: Start date must be before or equal to end date.")
                    continue

                # Check if all dates in the range are available
                all_dates_available = True
                current_date = start_date
                while current_date <= end_date:
                    if current_date.strftime('%Y-%m-%d') not in available_dates:
                        all_dates_available = False
                        break
                    current_date += timedelta(days=1)

                if not all_dates_available:
                    print("Error: Some dates in the selected range are not available.")
                    continue

                # Calculate the number of nights client will stay
                num_nights = (end_date - start_date).days + 1

                pay_method = input_pay_method()

                price_per_head = transient["price_per_head"]
                total_cost = number_of_people * price_per_head * num_nights

                # Confirm reservation
                print()
                print("Reservation Details")
                print(f"Client Name: {client_name}")
                print(f"Reservation From: {date_from}")
                print(f"Reservation To: {date_to}")
                print(f"Payment method: {pay_method}")
                print(f"Number of People: {number_of_people}")
                print(f"Calculating cost for {number_of_people} people staying {num_nights} night/s at ₱{price_per_head} per person...")
                print("Total cost: ₱", total_cost, sep="")

                confirm = input_confirm()
                if confirm == "n":
                    continue

                # Update verified details on JSON
                current_date = start_date
                while current_date <= end_date:
                    date_key = current_date.strftime('%Y-%m-%d')
                    transient['availability'][date_key]['status'] = "RESERVED"
                    transient['availability'][date_key]['client_name'] = client_name
                    transient['availability'][date_key]['date_from'] = date_from
                    transient['availability'][date_key]['date_to'] = date_to
                    transient['availability'][date_key]['number_of_people'] = number_of_people
                    current_date += timedelta(days=1)

                # Save the updated data back to the JSON file
                with open(file_path, 'w') as file:
                    json.dump(transients, file, indent=4)

                print()
                print("Reservation confirmed and saved.")
                print(f"Dear Mr./Ms. {client_name}, please proceed to {transient['location']} on {date_from} and enjoy your stay until {date_to}.")
                print("Thank you for trusting The Cozy Cabin.")
                break

            except ValueError:
                print("Invalid input. Please enter the number of people as an integer.")

        elif ans_input in ["n", "no"]:
            print()
            print("Returning to main menu.")
            return 0
        else:
            print("Invalid input. Please enter yes/no or y/n.")

def input_reserve_date(message, available_dates):
    while True:
        try:
            choice = int(input(message))
            if choice < 1 or choice > len(available_dates):
                print("Invalid Input. Please enter a number from 1 to", len(available_dates))
            else:
                date = available_dates[choice - 1]
                break
        except ValueError:
            print("Invalid input. Please enter a number.")
    return date
    pass

def input_pay_method():
    while True:
        print("\nAvailable Payment Methods")
        print("1. GCASH")
        print("2. PayMaya")
        pay_method = input("Select a payment method: ")
        if pay_method == "1":
            return "GCASH"
        elif pay_method == "2":
            return "PayMaya"
        else:
            print("\nInvalid! Please select one of the options.")
    pass

def input_confirm():
    while True:
        # Confirmation
        ans_input = input("Would you like to proceed? (y/n): ").strip().lower()
        if ans_input in ["y", "yes"]:
            return "y"
        elif ans_input in ["n", "no"]:
            return "n"
        else:
            print("Invalid input. Please enter yes/no or y/n.")
    pass

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
            try:
                choice = int(input("Enter a number from the menu: "))
            except ValueError:
                print("Invalid Input. Please enter a valid number.")
                continue

            if choice == 1:
                self.select_transient()
            elif choice == 2:
                self.sort_menu()
            elif choice == 3:
                self.filter_menu()
            elif choice == 4:
                exit(0)
            else:
                print("Invalid Input. Please enter a number from 1 to 4.")

    def select_transient(self):
        show_transient_table(self.transients)
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

            try:
                choice_sort = int(input("Enter a number from the menu: "))
                if choice_sort == 1:
                    sorted_transients = sort_transients(self.transients, 1)
                    show_transient_table(sorted_transients)
                elif choice_sort == 2:
                    sorted_transients = sort_transients(self.transients, 2)
                    show_transient_table(sorted_transients)
                elif choice_sort == 3:
                    show_transient_table(self.transients)
                elif choice_sort == 4:
                    break
                else:
                    print("Invalid Input. Please enter a number from 1 to 4.")
            except ValueError:
                print("Invalid Input. Please enter a valid number.")

    def filter_menu(self):
        choice_filter = 0
        while choice_filter != 3:
            print("\nFilter")
            print("1. Filter by transient name")
            print("2. Filter by address")
            print("3. Go back to Main Menu")
            try:
                choice_filter = int(input("Enter a number from the menu: "))
            except ValueError:
                print("Invalid Input. Please enter a valid number.")
                continue

            if choice_filter in [1, 2]:
                filter_query = input("Enter your filter query: ").strip()
                if filter_query:
                    filtered_transients = filter_transients(self.transients, choice_filter, filter_query)
                    if filtered_transients:
                        show_transient_table(filtered_transients)
                    else:
                        print(f"\nNo transients found matching the query: {filter_query}")
                else:
                    print("Filter query cannot be empty.")
            elif choice_filter == 3:
                break
            else:
                print("Invalid Input. Please enter a number from 1 to 3.")

def main():
    # Load JSON file
    transients = load_json(file_path)

    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 110

    # Print title
    print("The Cozy Cabin".center(terminal_width))
    print("Where Every Stay Feels Like Home".center(terminal_width))

    # Show the table
    show_transient_table(transients)

    # Instantiate and display the menu
    menu = Menu(transients)
    menu.display_menu()

if __name__ == "__main__":
    main()
