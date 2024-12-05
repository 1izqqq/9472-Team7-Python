import re
from prettytable import PrettyTable
from datetime import datetime, timedelta
from util.file_reader import FileReader
from util import printing_methods

def show_available_dates(transient):
    print(f"Name: {transient['name']}")
    print(f"Description: {transient['description']}")
    print(f"Please check available dates for {transient['name']}:")
    print()

    available_dates = []
    available_dates_table = PrettyTable()
    available_dates_table.field_names = ["ID", "Dates", "Status"]

    index = 0

    for date, details in transient['availability'].items():
        status = details['status'].upper()
        if status != "RESERVED":
            index += 1
            available_dates_table.add_row([index, date, status])
            available_dates.append(date)

    if len(available_dates) == 0:
        print("This transient has no available dates.")
        return None

    print(available_dates_table)
    return set(available_dates)

def reserve_dates(transient, available_dates, transients, reservation_file='transient_list.json'):
    available_dates_list = list(available_dates)
    available_dates_list.sort()
    while True:
        ans_input = input("Would you like to reserve? (y/n) ").strip().lower()
        if ans_input in ["y", "yes"]:
            ask_reservation_form(available_dates_list, transient, transients, reservation_file)
            return
        elif ans_input in ["n", "no"]:
            print()
            print("Returning to main menu.")
            return 0
        else:
            print("Invalid input. Please enter yes/no or y/n.")

def ask_reservation_form(available_dates_list, transient, transients, reservation_file='transient_list.json'):
    while True:
            print ( "\nReservation Form" )

            # Reservation details
            client_name = input_name ( )
            start_date = enter_date(available_dates_list, "Enter ID to select reservation start date: ")
            end_date = enter_date(available_dates_list, "Enter ID to select reservation end date: ")
            num_nights = get_number_of_nights(start_date,end_date)
            if num_nights == -1:
                continue
            pay_method = input_pay_method ( )
            number_of_people = input_number_of_people ( )
            price_per_head = transient [ "price_per_head" ]
            total_cost = number_of_people * price_per_head * num_nights
            printing_methods.show_reservation_details ( client_name , start_date , end_date , pay_method , number_of_people ,
                                                        num_nights , price_per_head , total_cost )
            confirm = input_confirm ( )
            if confirm == "n" :
                continue

            update_values_to_file(start_date, end_date, transient, client_name, number_of_people, transients, reservation_file)

            confirmation_message = (
                f"Reservation confirmed and saved.\n"
                f"Dear Mr./Ms. {client_name}, please proceed to {transient [ 'location' ]} on {start_date} and enjoy your stay until {end_date}.\n"
                "Thank you for trusting The Cozy Cabin."
            )
            print ("\n" + confirmation_message )
            return confirmation_message

def get_number_of_nights(start, end):
    start_date = datetime.strptime ( start , '%Y-%m-%d' )
    end_date = datetime.strptime ( end , '%Y-%m-%d' )
    if start_date > end_date :
        print ( "Error: Start date must be before or equal to end date." )
        return -1
    return (end_date - start_date).days + 1

def update_values_to_file(start_date, end_date, transient, client_name, number_of_people, transients, reservation_file):
    current_date = datetime.strptime ( start_date , '%Y-%m-%d' )
    while current_date <= datetime.strptime ( end_date , '%Y-%m-%d' ) :
        date_key = current_date.strftime ( '%Y-%m-%d' )
        transient [ 'availability' ] [ date_key ] [ 'status' ] = "RESERVED"
        transient [ 'availability' ] [ date_key ] [ 'client_name' ] = client_name
        transient [ 'availability' ] [ date_key ] [ 'date_from' ] = start_date
        transient [ 'availability' ] [ date_key ] [ 'date_to' ] = end_date
        transient [ 'availability' ] [ date_key ] [ 'number_of_people' ] = number_of_people
        current_date += timedelta ( days = 1 )

    # Save the updated data back to the JSON file
    FileReader.save_json ( transients , reservation_file )

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

def input_name():
    while True:
        client_name = input("Enter client name: ").strip()
        # Client name must not contain any integer
        if not re.match("^[A-Za-z\\s\\-]+$", client_name):
            print("Invalid name! Client name should not contain numbers or special characters. Please try again.")
        else:
            return client_name

def input_confirm():
    while True:
        ans_input = input("Would you like to proceed? (y/n): ").strip().lower()
        if ans_input in ["y", "yes"]:
            return "y"
        elif ans_input in ["n", "no"]:
            return "n"
        else:
            print("Invalid input. Please enter yes/no or y/n.")

def input_number_of_people():
    while True:
        number_of_people = input("Enter number of people: ").strip()

        if not number_of_people.isdigit():
            print("Please enter a valid integer for the number of people. Please try again.")
            continue

        number_of_people = int(number_of_people)

        if number_of_people <= 0:
            print("Number of people must be greater than 0. Please try again.")
            continue

        return number_of_people

def enter_choice(min_num, max_num, message):
    while True:
        try:
            choice = int(input(message))
            if choice < min_num or choice > max_num:
                print("Invalid Input. Please enter a number from ",min_num, "to", max_num)
            else:
                return choice
        except ValueError:
            print("Invalid Input. Please enter a valid number.")

def enter_date(available_dates_list, message):
    return available_dates_list[(enter_choice(1, len(available_dates_list), message)) - 1]
