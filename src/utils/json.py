import json


def write_json(data, output_file: str) -> None:
    """
    Writes data to a JSON file.

    This function takes data, a directory for output, and a filename, then writes the data into a JSON file at the specified location.

    Parameters:
    data: The data to write to the file.
    output_directory (str): The directory to write the file to.
    filename (str): The name of the file to write.
    """
    with open(output_file, "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_json(file_path: str):
    """
    Loads a JSON file.

    returns data in the JSON file.

    Do not use this function to load tag_tree.json.
    please use loadTagTree() instead.
    """
    with open(file_path, "r", encoding='utf-8') as file:
        data = json.load(file)
    return data