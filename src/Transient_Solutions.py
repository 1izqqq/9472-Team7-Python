from prettytable import PrettyTable

# Data setup
transients = [
    {"id": 1, "name": "Vista De Pino Transient House", "location": "31 Upper QM Baguio City", "price_per_head": 500, "contact": "09293375472"},
    {"id": 2, "name": "Analyn's Transient House", "location": "15 Happy Homes Campo Sioco Baguio City", "price_per_head": 550, "contact": "09486591743"},
    {"id": 3, "name": "Transient 3", "location": "23 Palispis Highway Baguio City", "price_per_head": 530, "contact": "09354726856"},
]

def show_transient_table():
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Location", "Price/Head", "Contact"]
    for transient in transients:
        table.add_row([transient["id"], transient["name"], transient["location"], f"₱{transient['price_per_head']}",
                       transient["contact"]])
    print(table)

def main():
    show_transient_table()

if __name__ == "__main__":
    main()