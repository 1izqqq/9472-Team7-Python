from util import printing_methods

def sort_transients_price(transients, sort_choice):
    if sort_choice == "asc":
        return sorted(transients, key=lambda x: x["price_per_head"])
    elif sort_choice == "desc":
        return sorted(transients, key=lambda x: x["price_per_head"], reverse=True)


def filter_transients(transients, filter_choice, filter_query):
    if filter_choice == 1:
        return [t for t in transients if filter_query.lower() in t["name"].lower()]
    elif filter_choice == 2:
        return [t for t in transients if filter_query.lower() in t["location"].lower()]
    return transients