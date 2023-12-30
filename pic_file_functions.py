# contains functions for processing picture files and metadata files.

import os
from shutil import copy2
import classes
from linecache import getline
from PIL import Image

def parsePicture(filePath: str) -> classes.PicData:
    """
    Extracts and returns information about a picture.

    This function opens a picture file, extracts its information, and stores it in a PicData object.

    Parameters:
    filePath (str): The path to the picture file.

    Returns:
    picData (classes.PicData): A PicData object containing the extracted information.
    """
    with Image.open(filePath) as img:# get resolution
        resolution = img.size
    del img # clear memory

    fileName = os.path.basename(filePath)
    name = fileName.split(".")# seprate the file name and file extention
    name.pop()
    name = str(name[0])
    parts = name.split("_p")# apart id and ordinal number
    pid = parts[0]
    ordNum = 1
    if len(parts) > 1:
        ordNum += int(parts[1])
    # create a PicData object then store the information
    Data = classes.PicData(pid, ordNum)
    Data.setSource("picture")
    Data.addResolution({ordNum:resolution})
    Data.addSize({ordNum:os.path.getsize(filePath)})
    Data.addFileName({ordNum:fileName})
    Data.addDirectory(os.path.dirname(filePath))
    return Data

def parseMetadata(filePath: str) -> classes.PicData:
    """
    Parses a metadata file and returns a PicData object.

    This function reads a metadata file line by line, extracts the metadata, and stores it in a PicData object.

    Parameters:
    path (str): The path to the metadata file.

    Returns:
    classes.PicData: A PicData object containing the metadata from the file.
    """
    tags = []
    Data = classes.PicData(getline(filePath, 2).strip())
    Data.setSource("metadata")
    Data.addDirectory(os.path.dirname(filePath))
    Data.addMetadata()
    Data.addTitle(getline(filePath, 5).strip())
    Data.addUser(getline(filePath, 8).strip())
    Data.addUserId(getline(filePath, 11).strip())

    lineNum = 17
    while True:
        if getline(filePath, lineNum) != "\n":
            # read and store tags
            tags.append(getline(filePath, lineNum).strip())
        else:
            # all tags read, store them in picData
            Data.addTags(tags)
            # read and store description
            Data.addDate(getline(filePath, lineNum + 2).strip())
            lines = []
            lineNum += 6
            while True:
                line = getline(filePath, lineNum)
                if line:
                    # read and store description line by line
                    lines.append(line)
                else:
                    # all description read, store them in picData
                    Data.addDescription(''.join(lines))
                    return Data
                lineNum += 1
        lineNum += 1

def getAllData(directory: str) -> dict:
    """
    Collects all metadata and picture information from a given directory.

    This function iterates over all files in the specified directory. If a file is a metadata file, it extracts the metadata and stores it in the data dictionary. If a file is a picture, it extracts the picture information and also stores it in the data dictionary.

    Parameters:
    directory (str): The directory to collect data from.

    Returns:
    dict: A dictionary containing all collected data.
    """

    data = {}
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
                PicMetadata = parseMetadata(filePath)
                pid = PicMetadata.getPid()
                # check metadata is already in data or not
                if pid in data:
                    # pid exist
                    data[pid] = PicMetadata.updateToDict(data[pid])
                else:
                    # pid not exist
                    data.update(PicMetadata.toDict())

            # process pictures
            else:
                PicMetadata = parsePicture(filePath)
                pid = PicMetadata.getPid()
                if pid in data:# pid exist
                    data[pid] = PicMetadata.updateToDict(data[pid])
                else:# pid not exist
                    data.update(PicMetadata.toDict())
    print("\n")
    return data

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
