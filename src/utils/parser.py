from PIL import Image
import os
from linecache import getline
import json

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
    Parses a metadata file and returns a PicData object.

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