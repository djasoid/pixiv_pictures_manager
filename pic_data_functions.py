import json
import program_objects as progObjs

# the program will generate four json files to store pic data
# 1. Metadata.json: contains all metadata
# 2. TagIndex.json: contains all tags and pids that contain the tags
# 3. IllustratorIndex.json: contains all illustrators info
# 4. NoMetadata.json: contains all pids without metadata

def writeJson(data, outputFile: str) -> None:
    """
    Writes data to a JSON file.

    This function takes data, a directory for output, and a filename, then writes the data into a JSON file at the specified location.

    Parameters:
    data: The data to write to the file.
    output_directory (str): The directory to write the file to.
    filename (str): The name of the file to write.
    """
    with open(outputFile, "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print (f"write to {outputFile} successfully")

def loadJson(filePath: str):
    """
    Loads a JSON file.

    returns data in the JSON file.

    Do not use this function to load tag_tree.json.
    please use loadTagTree() instead.
    """
    with open(filePath, "r", encoding='utf-8') as file:
        data = json.load(file)
    return data

def loadTagTree(tagTreeFile: str = "tag_tree.json") -> progObjs.TagTree:
    """
    Initializes a TagTree object from a JSON file.

    This function takes in a JSON file and returns a TagTree object.

    Parameters:
    tagTreeFile (str): The JSON file to load.

    Returns:
    classes.TagTree: A TagTree object.
    """
    with open(tagTreeFile, "r", encoding='utf-8') as file:
        tagTreeDict = json.load(file)
    Tree = progObjs.TagTree(tagTreeDict)
    del tagTreeDict # clear memory
    return Tree