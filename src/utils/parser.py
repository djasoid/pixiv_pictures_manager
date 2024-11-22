from PIL import Image
import os
from linecache import getline
import json
import csv

def parse_picture(file_path: str) -> tuple:
    """
    Extracts and returns information about a picture.

    This function opens a picture file, extracts its information, and stores it in a PicData object.

    Parameters:
    filePath (str): The path to the picture file.

    Returns:
    a tuple: A tuple containing the picture information.
    """
    with Image.open(file_path) as img:# get resolution
        resolution = img.size

    file_name = os.path.basename(file_path)
    name = file_name.split(".")# seprate the file name and file extention
    file_type = name.pop()
    name = str(name[0])
    parts = name.split("_p")# apart id and ordinal number
    pid = int(parts[0])
    if len(parts) == 1:
        num = 0
    else:
        num = int(parts[1])
    width = resolution[0]
    height = resolution[1]
    size = os.path.getsize(file_path)
    directory = os.path.dirname(file_path)

    return pid, num, directory, file_name, file_type, width, height, size

def parse_metadata(file_path: str) -> tuple:
    """
    Parses a metadata file and returns a tuple.

    This function reads a metadata file line by line, extracts the metadata, and stores it in a PicData object.

    Parameters:
    path (str): The path to the metadata file.

    Returns:
    tuple: A tuple containing the metadata information.
    """
    tags = {}
    xRestrict = "allAges"
    pid = int(getline(file_path, 2).strip())
    title = getline(file_path, 5).strip()
    user = getline(file_path, 8).strip()
    user_id = int(getline(file_path, 11).strip())

    line_num = 17
    while True: # read tags
        if getline(file_path, line_num) != "\n":
            tags.update({getline(file_path, line_num).strip(): "metadata"})
        else:
            if "#R-18" in tags:
                xRestrict = "R-18"
            elif "#R-18G" in tags:
                xRestrict = "R-18G"
            tags = json.dumps(tags, ensure_ascii=False) # convert tags to json string
            date = getline(file_path, line_num + 2).strip()
            description_lines = []
            line_num += 6
            break
        line_num += 1
    while True: # read description
        line = getline(file_path, line_num)
        if line:
            description_lines.append(line)
        else:
            description = '\n'.join(description_lines)
            return pid, title, tags, description, user, user_id, date, xRestrict
        line_num += 1

def parse_csv(file_path: str) -> list[tuple]:
    """
    Parses a CSV file and returns a list of tuples.

    This function reads a CSV file line by line, extracts the metadata, and stores it in a list of PicData objects.

    Parameters:
    path (str): The path to the CSV file.

    Returns:
    list: A list containing the metadata information.
    """
    pics = []
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            pid = int(row[0])
            tags = ["#" + tag for tag in row[1].split(',')]
            tags_transl = ["#" + tag for tag in row[2].split(',')]
            user = row[3]
            user_id = int(row[4])
            title = row[5]
            description = row[6]
            bookmarks = int(row[9])
            like = int(row[11])
            view = int(row[12])
            comment = int(row[13])
            xRestrict = row[16]
            date = row[17]
            pics.append((
                pid, 
                tags, 
                tags_transl, 
                user, 
                user_id,
                title,
                description, 
                bookmarks,
                like,
                view,
                comment,
                xRestrict, 
                date, 
            ))
    return pics