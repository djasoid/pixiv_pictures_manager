# This file contains all json related functions will be used in the program
# v2.0 (Changed the data structure for storing data, now using a dictionary instead of a list for better performance. Added documentation strings for all functions and implemented the collection of illustrator data.)

import os
import json
import shutil
import classes
import linecache
from PIL import Image

# ----------------------code for testing----------------------
PIC_FOLDER = "D:/Pixiv_Pictures"
PIC_BASE = "D:/Pixiv_Pictures/pixiv"
METADATA_FILE = "D:/Pixiv_Pictures/Metadata.json"
NEW_PIC_BASE = "C:/Users/Exusiai/Downloads/pixiv"
# ----------------------code for testing----------------------

def getPicInfo(filePath: str) -> tuple:
    """
    Extracts and returns information about a picture.

    This function opens a picture file, extracts its resolution, file type, and other information, and returns these as a tuple.

    Parameters:
    filePath (str): The path to the picture file.

    Returns:
    tuple: A tuple containing the picture's ID, ordinal number, file type, resolution, and size.
    """
    resolution = Image.open(filePath).size
    fileName = os.path.basename(filePath)
    fileName = fileName.split(".")# seprate the file name and file extention
    fileType = fileName[1]
    fileName.pop()
    fileName = str(fileName[0])
    parts = fileName.split("_p")# apart id and ordinal number
    id_part = int(parts[0])
    number_part = 1
    if len(parts) > 1:
        number_part = int(parts[1]) + 1
    return (id_part, number_part, fileType, resolution, os.path.getsize(filePath))

def parseMetadata(path: str) -> classes.PicData:
    """
    Parses a metadata file and returns a PicData object.

    This function reads a metadata file line by line, extracts the metadata, and stores it in a PicData object.

    Parameters:
    path (str): The path to the metadata file.

    Returns:
    classes.PicData: A PicData object containing the metadata from the file.
    """
    tags = []
    picData = classes.PicData(int(linecache.getline(path, 2).strip()))
    picData.addMetadata()
    picData.addTitle(linecache.getline(path, 5).strip())
    picData.addUser(linecache.getline(path, 8).strip())
    picData.addUserId(linecache.getline(path, 11).strip())

    for i in range(17, 1000):
        if linecache.getline(path, i) == "\n":
            picData.addTags(tags)
            picData.addDate(linecache.getline(path, i + 2).strip())
            lines = []
            for line_num in range(i+6, 1000):
                line = linecache.getline(path, line_num)
                if line:
                    lines.append(line)
                else: 
                    picData.addDescription(''.join(lines))
                    return picData
        else:
            tags.append(linecache.getline(path, i).strip())

def getAllData(directory: str, data: dict = {}) -> dict:
    """
    Collects all metadata and picture information from a given directory.

    This function iterates over all files in the specified directory. If a file is a metadata file, it extracts the metadata and stores it in the data dictionary. If a file is a picture, it extracts the picture information and also stores it in the data dictionary.

    Parameters:
    directory (str): The directory to collect data from.
    data (dict, optional): An existing dictionary to add data to. Defaults to an empty dictionary.

    Returns:
    dict: A dictionary containing all collected data.
    """
    processed_files = 0
    
    # iterate every file in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:

            # print progress
            processed_files += 1
            print(f'Processed {processed_files} files', end='\r')

            # get file path
            filePath = os.path.join(root, file)

            # process metadata file
            if file.endswith(".txt"):
                metadata = parseMetadata(filePath)
                pid = str(metadata.getPid())
                metadataInDict = classes.PicData.getMetadata(metadata)
                # check metadata is already in data or not
                if pid in data:
                    # pid exist
                    metadataInDict[pid]["count"] = data[pid]["count"]
                    metadataInDict[pid]["resolution"] = data[pid]["resolution"]
                    metadataInDict[pid]["size"] = data[pid]["size"]
                    metadataInDict[pid]["fileType"] = data[pid]["fileType"]
                    metadataInDict[pid]["path"] = data[pid]["path"]
                    # above is the information not in metadata(.txt file)
                    data.update(metadataInDict)
                else:
                    data.update(metadataInDict)

            # process pictures
            else:
                info = getPicInfo(filePath)
                pid = str(info[0])
                if pid in data:# pid exist
                    data[pid]["resolution"].update({info[1]:info[3]})
                    data[pid]["size"].update({info[1]:info[4]})
                    if data[pid]["count"] < info[1]:
                        data[pid]["count"] = info[1]
                    if data[pid]["fileType"] == None:
                        data[pid]["fileType"] = info[2]
                    if data[pid]["path"] == None:
                        data[pid]["path"] = filePath
                else:# pid not exist
                    metadata = classes.PicData(info[0], info[1])
                    metadata.addResolution({info[1]:info[3]})
                    metadata.addSize({info[1]:info[4]})
                    metadata.addType(info[2])
                    metadata.addPath(filePath)
                    data.update(classes.PicData.getMetadata(metadata))
    print("\n")
    return data

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

def isR18(metadata: dict) -> bool:
    """
    Checks if a picture contains the R18 tag.

    This function takes a dictionary of picture information and checks if it contains the R18 tag. If it does, it returns True, otherwise it returns False.

    Parameters:
    metadata (dict): A dictionary containing picture information.

    Returns:
    bool: True if the picture contains the R18 tag, False otherwise.
    """
    for tag in metadata["tags"]:
        if tag == "#R-18":
            return True
    return False

def getTagCount(metadataDict: dict) -> tuple:
    """
    Counts the number of times each tag appears in metadataDict.

    This function accepts a dictionary of metadata and extracts all the tags present in the file. It then counts the number of times each tag appears and returns a tuple with two dictionaries. The first dictionary contains all ages tags and the second dictionary contains R-18 tags. In the dictionary, the tag is the key and the number of times it appears is the value.

    Parameters:
    metadataDict (dict): A dictionary of metadata.

    Returns:
    tuple: A tuple containing two dictionaries. The first dictionary contains all ages tags and the second dictionary contains R-18 tags.
    """
    tags = {}
    r18tags = {}
    r18pid = []

    # iterate every picture handle all ages tags 
    for pid in metadataDict:
        data = metadataDict[pid]
        # check it has metadata or not
        if data["metadata"] != False:
            if isR18(data):# check if it is R18
                r18pid.append(data["pid"])# add pid to r18pid list
            else:# not R18
                for tag in data["tags"]:
                    if tag in tags:
                        tags[tag] += 1
                    else:
                        tags[tag] = 1

    # handle R18 tags
    for pid in r18pid:# iterate every R18 picture
        pid = str(pid)
        for tag in metadataDict[pid]["tags"]:# iterate every tag in the picture
            if tag in tags:# check if the tag is already in tags
                pass
            else:
                if tag in r18tags:
                    r18tags[tag] += 1
                else:
                    r18tags[tag] = 1
    return (tags, r18tags)

def sortTags(tags: dict) -> tuple:
    """
    Sorts a dictionary of tags and returns a sorted tuple.

    This function takes a dictionary of tags and returns a sorted tuple where each element is a dictionary of a tag and its count. The tuple is sorted in decreasing order of count.

    Parameters:
    tags (dict): A dictionary of tags.

    Returns:
    tuple: A sorted tuple where each element is a dictionary of a tag and its count.
    """
    sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)
    return sorted_tags

def mergeDirs(src: str, dst: str) -> None:
    """
    Copies all files from one directory to another.

    This function takes two directories, copies all files from the source to the destination. If a file already exists in the destination, it is skipped.

    Parameters:
    src (str): The source directory.
    dst (str): The destination directory.
    """

    for src_dir, dirs, files in os.walk(src):
        dst_dir = src_dir.replace(src, dst, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                continue
            shutil.copy2(src_file, dst_dir)

def getPicPath(metadataDict: dict, pid: int) -> str:
    """
    Returns the path of a picture given its pid.

    This function takes a dictionary of metadata and a pid, and returns the path of the picture with the given pid.

    Parameters:
    metadataDict (dict): A dictionary of metadata.
    pid (int): The pid of the picture.

    Returns:
    str: The path of the picture.
    """
    return metadataDict[pid]["path"]

def loadMetadata(metadataFile: str) -> dict:
    """
    Loads a metadata file and returns a list of dictionaries of picture info in the file.

    This function should be used when initializing the program.

    Parameters:
    metadataFile: The metadata file to load.

    Returns:
    list: A list of dictionaries of picture info in the file.
    """
    with open (metadataFile, "r", encoding='utf-8') as file:
        metadataDict = json.load(file)
    return metadataDict

def getIllustratorInfo(metadataDict: dict) -> dict:
    """
    Returns a dictionary with illustrator info (id, name, pidList).

    This function takes in a metadata list and returns a dictionary with illustrator info (id, name, pidList).

    Parameters:
    metadataDict: A metadata list.

    Returns:
    dict: A dictionary with illustrator info (id, name, pidList).
    """
    illustratorDict = {}
    for pid in metadataDict:# iterate every picture info
        data = metadataDict[pid]
        if data["metadata"] != False:
            uid = str(data["userId"])
            if uid in illustratorDict:# check if the illustrator is already in the dictionary
                if data["user"] not in illustratorDict[uid]["name"]:# check if the name is already in the dictionary
                    illustratorDict[uid]["name"].append(data["user"])# add name to the dictionary
                illustratorDict[uid]["pidList"].append(data["pid"])# add pid to the dictionary
            else:# illustrator not in the dictionary
                illustratorDict.update({uid: {"uid": data["userId"], "name":[data["user"]], "pidList":[data["pid"]]}})
    return illustratorDict