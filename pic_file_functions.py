import os
from shutil import copy2
from linecache import getline
from PIL import Image
from pic_data_functions import PicDatabase
import json

def parsePicture(filePath: str) -> tuple:
    """
    Extracts and returns information about a picture.

    This function opens a picture file, extracts its information, and stores it in a PicData object.

    Parameters:
    filePath (str): The path to the picture file.

    Returns:
    a tuple: A tuple containing the picture information.
    """
    with Image.open(filePath) as img:# get resolution
        resolution = img.size

    fileName = os.path.basename(filePath)
    name = fileName.split(".")# seprate the file name and file extention
    fileType = name.pop()
    name = str(name[0])
    parts = name.split("_p")# apart id and ordinal number
    pid = int(parts[0])
    if len(parts) == 1:
        num = 0
    else:
        num = int(parts[1])
    width = resolution[0]
    height = resolution[1]
    size = os.path.getsize(filePath)
    directory = os.path.dirname(filePath)

    return pid, num, directory, fileName, fileType, width, height, size

def parseMetadata(filePath: str) -> tuple:
    """
    Parses a metadata file and returns a PicData object.

    This function reads a metadata file line by line, extracts the metadata, and stores it in a PicData object.

    Parameters:
    path (str): The path to the metadata file.

    Returns:
    tuple: A tuple containing the metadata information.
    """
    tags = []
    pid = getline(filePath, 2).strip()
    title = getline(filePath, 5).strip()
    user = getline(filePath, 8).strip()
    userId = getline(filePath, 11).strip()

    lineNum = 17
    while True: # read tags
        if getline(filePath, lineNum) != "\n":
            tags.append({getline(filePath, lineNum).strip(): "metadata"})
        else:
            tags = json.dumps(tags, ensure_ascii=False) # convert tags to json string
            date = getline(filePath, lineNum + 2).strip()
            descriptionLines = []
            lineNum += 6
            break
        lineNum += 1
    while True: # read description
        line = getline(filePath, lineNum)
        if line:
            descriptionLines.append(line)
        else:
            description = ''.join(descriptionLines)
            return pid, title, tags, description, user, userId, date
        lineNum += 1


def getAllData(directory: str) -> None:
    """
    Collects all metadata and picture information from a given directory.

    This function iterates over all files in the specified directory. If a file is a metadata file, it extracts the metadata and stores it in the data dictionary. If a file is a picture, it extracts the picture information and also stores it in the data dictionary.

    Parameters:
    directory (str): The directory to collect data from.

    Returns:
    dict: A dictionary containing all collected data.
    """

    processedFiles = 0
    database = PicDatabase()
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            processedFiles += 1
            print(f'Processed {processedFiles} files', end='\r')

            filePath = os.path.join(root, file)
            if file.endswith(".txt"):
                metadata = parseMetadata(filePath)
                database.insertMetadata(*metadata)
            
            elif file.endswith(".webp"): # ignore webp files because they cannot be processed
                continue

            else:
                imageData = parsePicture(filePath)
                database.insertImageData(*imageData)
    print("\n")
    database.closeDatabase()

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
            copy2(src_file, dst_dir)

if __name__ == "__main__":
    getAllData("C:\\Users\\Exusiai\\Downloads\\pixiv")
    print("All files processed successfully.")