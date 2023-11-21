# This file contains all json related functions will be used in the program
# v1.3 (add tag count and sort function)

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

def isR18(metadata):
    """This function takes in a dictionary of picture informations and check if it contains R18 tag. If it does, return True, else return False"""
    for tag in metadata["tags"]:
        if tag == "#R-18":
            return True
    return False

def getTagCount(metadataFile):
    """This function accepts a metadata file in the .json format and extracts all the tags present in the file. It then counts the number of times each tag appears and returns a tuple with two dictionary, the first dictionary contains all ages tags and the second dictionary contains R-18 tags. in the dictionary, the tag is the key and the number of times it appears is the value."""
    tags = {}
    r18tags = {}
    r18pid = []

    # read metadata file
    with open (metadataFile, "r", encoding='utf-8') as file:
        metadata = json.load(file)

    # iterate every picture handle all ages tags 
    for data in metadata:
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
        else:
            pass

    # handle R18 tags
    for pid in r18pid:# iterate every R18 picture
        result = pidSearch(metadata, pid)# find the picture in metadata
        for tag in metadata[result[1]]["tags"]:# iterate every tag in the picture
            if tag in tags:# check if the tag is already in tags
                pass
            else:
                if tag in r18tags:
                    r18tags[tag] += 1
                else:
                    r18tags[tag] = 1
    return (tags, r18tags)

def sortTags(tags):
    """This function takes in a dictionary of tags then returns a sorted tuple with every element in it is a dictionary of tag and its count. The tuple is sorted in decreasing order of count"""
    sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)
    return sorted_tags

def storeTags(tags, output_path, filename = "Tags.json"):
    """This function takes in a list of tuple of counted and sorted tags and a path for output, write the tuple into a json file"""
    output_file = os.path.join(output_path, filename)
    with open(output_file, "w", encoding='utf-8') as file:
        json.dump(tags, file, indent=4, ensure_ascii=False)
    print (f"\nthe file is at {output_file}")

# ----------------------code for testing----------------------
# tagcount = getTagCount(PIC_DATA)
# sorted_all_age_tags = sortTags(tagcount[0])
# sorted_r18_tags = sortTags(tagcount[1])
# storeTags(sorted_all_age_tags, os.path.dirname(PIC_DATA))
# storeTags(sorted_r18_tags, os.path.dirname(PIC_DATA), "R18Tags.json")
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

def isSorted(metadataFile):
    """This function takes in a list of dictionaries of pic info and check if the list is sorted in increasing order of pid"""
    with open (metadataFile, "r", encoding='utf-8') as file:
        metadata = json.load(file)
    count = 0
    for i in range(len(metadata) - 1):
        count += 1
        print(f'Processed {count}', end='\r')
        if metadata[i]["pid"] > metadata[i + 1]["pid"]:
            return False
    return True

# ----------------------code for testing----------------------
# test if the metadata file is sorted in increasing order of pid

# print (isSorted(PIC_DATA))
# ----------------------code for testing----------------------