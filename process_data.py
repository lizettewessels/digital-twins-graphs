import bibtexparser
import json
import os

# For every file located in the raw directory
for f in os.listdir("./data/raw"):

    # Load the .bib file
    with open(f"./data/raw/{f}", "r") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    
    # Convert to JSON
    bib_json = json.dumps(bib_database.entries, indent=4)
    
    # Ensure the target directory exists
    os.makedirs("./data/processed", exist_ok=True)

    # Create new file name
    file_name = f.replace(".bib", ".json")
    
    # Save the JSON data to a file
    with open(f"./data/processed/{file_name}", "w") as json_file:
        json_file.write(bib_json)
