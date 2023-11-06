# This file contains all functions will be used in the program
# v1.1 (implemented data collecting functions, using json file to store the data, data is sorted to increasing order of pid)

import os
import json
import classes
import linecache

def getPicInfo(fileName):
    """this function takes fileName of a picture and return a tuple (pid, ordinal number, file type) inside"""
    fileName = fileName.split(".")# seprate the file name and file extention
    fileType = fileName[1]
    fileName.pop()
    fileName = str(fileName[0])
    parts = fileName.split("_p")# apart id and ordinal number
    id_part = int(parts[0])
    number_part = 1
    if len(parts) > 1:
            number_part = int(parts[1]) + 1
    return (id_part, number_part, fileType)

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
    # use bisection recursive searching
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

def getAllPid(directory, output_path):
    """This function takes in the directory of pixiv pictures/metabeta file and a path for output, then create a json file to store all information, the information is sorted in increasing order of pid, outputed in output path. Use when initialize the management program"""
    processed_files = 0
    output_file = output_path + "Metadata.json"
    # initialize a list to store dictionaries of metabeta
    pids = []
    # iterate every file in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            processed_files += 1
            print(f'Processed {processed_files} files', end='\r')
            # process metadata file
            if file.endswith(".txt"):
                metadata = classes.PicData.getMetadata(parseMetadata(os.path.join(root, file)))
                if pids == []:
                    pids.append(metadata)
                # check metadata is already in pids or not
                result = pidSearch(pids, metadata["pid"])
                if result[0]:
                    # pid exist
                    metadata["count"] = pids[result[1]]["count"]
                    pids[result[1]] = metadata
                else:
                    pids.insert(result[1], metadata)
            # process pictures
            else:
                info = getPicInfo(file)
                result = pidSearch(pids, info[0])
                if pids == []:
                    metadata = classes.PicData(info[0], info[1])
                    metadata.addType(info[2])
                    metadata.addPath(os.path.join(root, file))
                    pids.append(classes.PicData.getMetadata(metadata))
                if result[0]:
                    if pids[result[1]]["count"] < info[1]:
                        pids[result[1]]["count"] = info[1]
                    if pids[result[1]]["type"] == None:
                        pids[result[1]]["type"] = info[2]
                    if pids[result[1]]["path"] == None:
                        pids[result[1]]["path"] = os.path.join(root, file)
                else:
                    metadata = classes.PicData(info[0], info[1])
                    metadata.addType(info[2])
                    metadata.addPath(os.path.join(root, file))
                    pids.insert(result[1], classes.PicData.getMetadata(metadata))
    # create a json file and put all information in it
    with open(output_file, "w") as file:
        json.dump(pids, file)

# ----------------------code for testing----------------------

# directory = "e:/pixiv" # put pixiv picture folder here
# output_path = "e:/" # put output folder path of json here
# output_file = output_path + "Metadata.json"
# print (f"Processing pictures in {directory}\n")
# getAllPid(directory, output_path)
# print ("\n")
# print (f"Finished! Output json file is {output_file}")

# ----------------------code for testing----------------------