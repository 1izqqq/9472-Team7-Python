import os
import json
from prettytable import PrettyTable
from datetime import datetime, timedelta

# File path where the JSON file is saved
file_path = 'transient_list.json'


# Load JSON file
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def show_transient_table(transients):
    main_table = PrettyTable()
    main_table.field_names = ["ID", "Name", "Address", "Price/Head", "Contact"]

    for transient in transients:
        main_table.add_row(
            [transient["id"],
             transient["name"],
             transient["location"],
             f"₱{transient['price_per_head']}",
             transient["contact"]])

    print(main_table)


def show_available_dates(transient):
    print(f"Name: {transient['name']}")
    print(f"Description: {transient['description']}")
    print(f"Please check available dates for {transient['name']}:")
    print()

    available_dates = []  # List holding available dates
    available_dates_table = PrettyTable()
    available_dates_table.field_names = ["Dates", "Status"]

    for date, details in transient['availability'].items():
        status = details['status'].upper()
        # Remove dates with "RESERVED" status
        if status != "RESERVED":
            available_dates_table.add_row([date, status])
            available_dates.append(date)

    # Print table
    print(available_dates_table)

    return set(available_dates)


def reserve_dates(transient, available_dates, transients):
    while True:
        ans_input = input("Would you like to reserve? (y/n) ").strip().lower()
        if ans_input in ["y", "yes"]:
            try:
                client_name = input("Enter client name: ").strip()
                date_from = input("Enter reservation start date (YYYY-MM-DD): ").strip()
                date_to = input("Enter reservation end date (YYYY-MM-DD): ").strip()
                number_of_people = int(input("Enter number of people: ").strip())

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

                # Confirm reservation
                print()
                print("Reservation Details")
                print(f"Client Name: {client_name}")
                print(f"Reservation From: {date_from}")
                print(f"Reservation To: {date_to}")
                print(f"Number of People: {number_of_people}")

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
                break

            except ValueError:
                print("Invalid input. Please enter the number of people as an integer.")
        elif ans_input in ["n", "no"]:
            print("Returning to main menu.")
            break
        else:
            print("Invalid input. Please enter yes/no or y/n.")


def main():
    transients = load_json(file_path)

    # This centers the title on the console
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 110

    # Print title
    print("The Cozy Cabin".center(terminal_width))
    print("Where Every Stay Feels Like Home".center(terminal_width))

    # Show the table
    show_transient_table(transients)

    # Prompt for user input
    print()
    print("Select a house you are interested in!")
    while True:
        try:
            user_input = input("Please input transient house's ID: ").strip()
            print()
            option = int(user_input)

            selected_transient = next((t for t in transients if t['id'] == option), None)
            if selected_transient:
                available_dates = show_available_dates(selected_transient)
                reserve_dates(selected_transient, available_dates, transients)
                break
            else:
                print("Invalid ID. Please enter a valid transient house ID!")

        except ValueError:
            print("Main Menu: Invalid input. Please enter a number.")


# Main Method
if __name__ == "__main__":
    main()
