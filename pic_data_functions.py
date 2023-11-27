# This file contains all pic data functions

import os
import json
import classes

# the program will generate four json files to store pic data
# 1. Metadata.json: contains all metadata
# 2. TagIndex.json: contains all tags and pids that contain the tags
# 3. IllustratorIndex.json: contains all illustrators info
# 4. NoMetadata.json: contains all pids without metadata

def writeJson(data, output_path: str, filename: str = "Metadata.json") -> None:
    """
    Writes a dictionary to a JSON file.

    This function takes a dictionary, a path for output, and a filename, then writes the dictionary into a JSON file at the specified location.

    Parameters:
    data (dict): The data to write to the file.
    output_path (str): The directory to write the file to.
    filename (str, optional): The name of the file to write. Defaults to "Metadata.json".
    """
    output_file = os.path.join(output_path, filename)
    with open(output_file, "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print (f"\nthe file is at {output_file}")

def loadMetadataFile(metadataFile: str) -> dict:
    """
    Loads a metadata file and returns a dictionary of picture info in the file.

    This function should be used when initializing the program.

    Parameters:
    metadataFile (str): The metadata file path to load.

    Returns:
    dict: A dictionary of picture info in the file.
    """
    with open (metadataFile, "r", encoding='utf-8') as file:
        metadataDict = json.load(file)
    return metadataDict

def loadTagTree(tagTreeFile: str) -> classes.TagTree:
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
    tagTree = classes.TagTree(tagTreeDict["标签"])
    tagTreeDict = None
    return tagTree

def loadIllustratorInfo(illustratorInfoFile: str) -> dict:
    """
    Loads a illustrator info file and returns a dictionary of illustrator info in the file.

    This function should be used when initializing the program.

    Parameters:
    illustratorInfoFile (str): The illustrator info file path to load.

    Returns:
    dict: A dictionary of illustrator info in the file.
    """
    with open (illustratorInfoFile, "r", encoding='utf-8') as file:
        illustratorInfo = json.load(file)
    return illustratorInfo

def loadNoMetadata(noMetadataFile: str) -> dict:
    """
    Loads a no metadata file and returns a dictionary of picture info in the file.

    This function should be used when initializing the program.

    Parameters:
    noMetadataFile (str): The no metadata file path to load.

    Returns:
    dict: A dictionary of picture info in the file.
    """
    with open (noMetadataFile, "r", encoding='utf-8') as file:
        noMetadata = json.load(file)
    return noMetadata