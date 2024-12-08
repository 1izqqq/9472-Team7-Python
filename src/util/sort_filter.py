from util import printing_methods

def sort_transients_price(transients, sort_choice):
    """
    Sorts a list of transients based on the price per head.

    Args:
        transients (list): A list of dictionaries where each dictionary represents a transient.
                           Each transient must have a "price_per_head" key with a numeric value.
        sort_choice (str): Sorting order. Use "asc" for ascending or "desc" for descending.

    Returns:
        list: A sorted list of transients based on price per head.
    """
    if sort_choice == "asc":
        return sorted(transients, key=lambda x: x["price_per_head"])
    elif sort_choice == "desc":
        return sorted(transients, key=lambda x: x["price_per_head"], reverse=True)


def filter_transients(transients, filter_choice, filter_query):
    """
    Filters a list of transients based on a search query applied to either the name or location.

    Args:
        transients (list): A list of dictionaries where each dictionary represents a transient.
                           Each transient must have "name" and "location" keys with string values.
        filter_choice (int): The filter criteria.
                             Use 1 to filter by name, or 2 to filter by location.
        filter_query (str): The search query to apply for filtering.

    Returns:
        list: A filtered list of transients based on the specified filter criteria and query.
    """
    if filter_choice == 1:
        return [t for t in transients if filter_query.lower() in t["name"].lower()]
    elif filter_choice == 2:
        return [t for t in transients if filter_query.lower() in t["location"].lower()]
    return transients