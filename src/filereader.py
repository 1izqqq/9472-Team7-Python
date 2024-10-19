import json

# Load JSON file
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Save the updated data back to the JSON file
def save_json(transients,file_path):
    with open(file_path, 'w') as file:
        json.dump(transients, file, indent=4)