# This file contains all functions will be used in the program
# v1.2 (1.metadata file now contains resolution and size information. 2. add function to add new data into existing metadata file. 3. add function to merge two directories)

import os
import json
import shutil
import classes
import linecache
from PIL import Image

# ----------------------code for testing----------------------
PIC_BASE = "D:/Pixiv_Pictures/pixiv"
PIC_DATA = "D:/Pixiv_Pictures/metadata.json"
NEW_PIC_BASE = "C:/Users/Exusiai/Downloads/pixiv"
# ----------------------code for testing----------------------

def getPicInfo(filePath):
    """this function takes the directory of a picture and return a tuple (pid, ordinal number, file type, resolution, size) containing the information of the picture"""
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

def parseMetadata(path):
    """this function takes the path of metadata file(.txt) and return a PicData which contains the data in the file"""
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

def pidSearch(list, pid, left = 0, right = None):
    """This function takes in a list of dictionary which stores metadata and a pid. If the pid is in the list, return a tuple of True and the index number of the dictionary holding the pid, if the pid is not exist in the list, return False and the index of dictionary which holds bigger pid in the list. The list must be sorted into increasing order of pid"""
    if right is None:
        right = len(list) - 1
    
    if left > right:
        return (False,left)
    
    mid = (left + right) // 2

    if list[mid]["pid"] == pid:
        return (True,mid)
    elif list[mid]["pid"] < pid:
        return pidSearch(list, pid, mid + 1, right)
    else:
        return pidSearch(list, pid, left, mid - 1)

def getAllData(directory, data = []):
    """This function takes in the directory of pixiv pictures/metabeta file and a list of existing data, return a list with all information, the information is sorted in increasing order of pid."""
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
                metadata = classes.PicData.getMetadata(parseMetadata(filePath))
                if data == []:
                    data.append(metadata)

                # check metadata is already in data or not
                result = pidSearch(data, metadata["pid"])
                if result[0]:
                    # pid exist
                    metadata["count"] = data[result[1]]["count"]
                    data[result[1]] = metadata
                else:
                    data.insert(result[1], metadata)

            # process pictures
            else:
                info = getPicInfo(filePath)
                result = pidSearch(data, info[0])# check if pid is already in data
                if data == []:
                    metadata = classes.PicData(info[0], info[1])
                    metadata.addResolution({info[1]:info[3]})
                    metadata.addSize({info[1]:info[4]})
                    metadata.addType(info[2])
                    metadata.addPath(filePath)
                    data.append(classes.PicData.getMetadata(metadata))
                    break
                elif result[0]:# pid exist
                    data[result[1]]["resolution"].update({info[1]:info[3]})
                    data[result[1]]["size"].update({info[1]:info[4]})
                    if data[result[1]]["count"] < info[1]:
                        data[result[1]]["count"] = info[1]
                    if data[result[1]]["fileType"] == None:
                        data[result[1]]["fileType"] = info[2]
                    if data[result[1]]["path"] == None:
                        data[result[1]]["path"] = filePath
                else:# pid not exist
                    metadata = classes.PicData(info[0], info[1])
                    metadata.addResolution({info[1]:info[3]})
                    metadata.addSize({info[1]:info[4]})
                    metadata.addType(info[2])
                    metadata.addPath(filePath)
                    data.insert(result[1], classes.PicData.getMetadata(metadata))
    return data

def writeJson(data, output_path):
    """This function takes in a list of dictionaries and a path for output, write the list into a json file"""
    output_file = os.path.join(output_path, "Metadata.json")
    with open(output_file, "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print (f"\nthe file is at {output_file}")

# ----------------------code for testing----------------------

# directory = "e:/pixiv" # put pixiv picture folder here
# output_path = "e:/" # put output folder path of json here
# output_file = output_path + "Metadata.json"
# print (f"Processing pictures in {directory}\n")
# getAllData(directory, output_path)
# print ("\n")
# print (f"Finished! Output json file is {output_file}")

# ----------------------code for testing----------------------

def getAllTags(metadataFile):
    """This function accepts a metadata file in the .json format and extracts all the tags present in the file. It then stores these tags in a text file located in the same directory"""
    fileName = "tag_list.txt"
    output = os.path.join(os.path.dirname(metadataFile),fileName)
    tags = []

    # read metadata file
    with open (metadataFile, "r", encoding='utf-8') as file:
        metadata = json.load(file)
    
    for data in metadata:
        # check it has metadata or not
        if data["metadata"] != False:
            for tag in data["tags"]:
                #check if tag is already existed or not
                if not tag in tags:
                    tags.append(tag)
                else:
                    pass
        else:
            pass
    
    # generate txt file with tags in it
    with open(output, "w", encoding='utf-8') as file:
        for item in tags:
            file.write(item + "\n")
    print (f"\nthe file is at {output}")

# ----------------------code for testing----------------------
# metadataFile = "E:/Metadata.json"
# getAllTags(metadataFile)
# print ("\nfinished!")
# ----------------------code for testing----------------------

def addNewData(directory, metadataFile = None):
    """This function takes in the directory of pixiv pictures/metabeta file and a metadata file path.
    If the metadata file is not specified, it will be created at the same directory of pixiv pictures folder.
    If the metadata file is specified, it will be used to store the new data."""
    # get metadata file path. metadata.json is at the same directory of pixiv pictures folder
    if metadataFile == None:
        metadataFile = os.path.join(os.path.dirname(directory), 'metadata.json')
        with open(metadataFile, 'w', encoding='utf-8') as file:
            json.dump([], file)  # create empty json file
    with open (metadataFile, "r", encoding='utf-8') as file:
        metadata = json.load(file)
    writeJson(getAllData(directory, metadata), os.path.dirname(metadataFile))
    print ("\nNew data added!")

def merge_dirs(src, dst):
    """This function takes in two directories, copy all files from src to dst, if the file already exist in dst, skip it"""
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

# ----------------------code for testing----------------------
# addNewData(NEW_PIC_BASE, PIC_DATA)
# merge_dirs(NEW_PIC_BASE, PIC_BASE)
# print ("\nfinished!")
# ----------------------code for testing----------------------