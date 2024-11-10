import json
import sqlite3
import os
import tag_tree as tree
from shutil import copy2
from linecache import getline
from PIL import Image
import dataclasses

def write_json(data, output_file: str) -> None:
    """
    Writes data to a JSON file.

    This function takes data, a directory for output, and a filename, then writes the data into a JSON file at the specified location.

    Parameters:
    data: The data to write to the file.
    output_directory (str): The directory to write the file to.
    filename (str): The name of the file to write.
    """
    with open(output_file, "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_json(file_path: str):
    """
    Loads a JSON file.

    returns data in the JSON file.

    Do not use this function to load tag_tree.json.
    please use loadTagTree() instead.
    """
    with open(file_path, "r", encoding='utf-8') as file:
        data = json.load(file)
    return data

def load_tag_tree(tag_tree_file: str = "tag_tree.json") -> tree.TagTree:
    """
    Initializes a TagTree object from a JSON file.

    This function takes in a JSON file and returns a TagTree object.

    Parameters:
    tagTreeFile (str): The JSON file to load.

    Returns:
    classes.TagTree: A TagTree object.
    """
    with open(tag_tree_file, "r", encoding='utf-8') as file:
        tag_tree_dict = json.load(file)
    tagTree = tree.TagTree(tag_tree_dict)
    return tagTree

class PicDatabase:
    def __init__(self):
        self.database = None
        self.cursor = None
        self.load_database()
        
    def load_database(self):
        """
        Load the database.
        """
        if os.path.exists("pic_data.db"):
            self.database = sqlite3.connect("pic_data.db")
            self.cursor = self.database.cursor()
        else:
            self.database = sqlite3.connect("pic_data.db")
            self.cursor = self.database.cursor()
            self.cursor.execute(
                '''CREATE TABLE imageData (
                    pid INT, 
                    num INT, 
                    directory TEXT, 
                    fileName TEXT, 
                    fileType TEXT,
                    width INT, 
                    height INT, 
                    size INT, 
                    PRIMARY KEY (pid, num)
                )'''
            )
            self.cursor.execute(
                '''CREATE TABLE metadata (
                    pid INT, 
                    title TEXT, 
                    tags TEXT,
                    description TEXT,
                    user TEXT,
                    userId INT,
                    date TEXT,
                    xRestrict TEXT,
                    bookmarkCount INT,
                    likeCount INT,
                    viewCount INT,
                    commentCount INT,
                    PRIMARY KEY (pid)
                )'''
            )
            self.cursor.execute(
                '''CREATE TABLE tagIndex (
                    tag TEXT,
                    pids TEXT,
                    PRIMARY KEY (tag)
                )'''
            )
            self.cursor.execute('''CREATE INDEX tag ON tagIndex (tag)''')
            self.cursor.execute('''CREATE INDEX dataPid ON metadata (pid)''')
            self.cursor.execute('''CREATE INDEX filePid ON imageData (pid)''')
    
    def insert_image_data(self, pid, num, directory, file_name, file_type, width, height, size):
        """
        Insert image data into the database.
        """
        self.cursor.execute("INSERT OR IGNORE INTO imageData VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (pid, num, directory, file_name, file_type, width, height, size)
                            )
        self.database.commit()
        
    def insert_metadata(
            self, 
            pid, 
            title, 
            tags, 
            description, 
            user, 
            user_id, 
            date,
            xRestrict, 
            bookmark_count=None, 
            like_count=None, 
            view_count=None, 
            comment_count=None
        ):
        """
        Insert metadata into the database.
        """
        self.cursor.execute(
            "INSERT OR IGNORE INTO metadata VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                pid, 
                title, 
                tags, 
                description, 
                user, 
                user_id, 
                date,
                xRestrict, 
                bookmark_count, 
                like_count, 
                view_count, 
                comment_count
            )
        )
        self.database.commit()
    
    def insert_tag_index(self, tag, pids):
        """
        Insert tag index into the database.
        """
        self.cursor.execute("INSERT OR IGNORE INTO tagIndex VALUES (?, ?)", (tag, json.dumps(pids)))
        self.database.commit()
    
    def insert_tag_index_dict(self, tag_index_dict: dict[str, list[str]]):
        """
        Insert tag index dictionary into the database.
        """
        for tag, pids in tag_index_dict.items():
            self.insert_tag_index(tag, pids)
        self.database.commit()
    
    def get_pids_by_tag(self, tag: str) -> set:
        """
        Get pids by tag.
        """
        self.cursor.execute("SELECT pids FROM tagIndex WHERE tag = ?", (tag))
        pidsJson = self.cursor.fetchone()
        if pidsJson:
            return set(json.loads(pidsJson[0]))
        else:
            return []
    
    def __del__(self):
        self.database.close()
    
    def get_tags(self, pid) -> dict:
        """
        Get tags of a picture.
        """
        self.cursor.execute("SELECT tags FROM metadata WHERE pid = ?", (pid))
        tags_json = self.cursor.fetchone()
        if tags_json:
            return json.loads(tags_json[0])
        else:
            return {}
        
    def get_pid_list(self) -> list:
        """
        Get a list of all pids in metadata.
        """
        self.cursor.execute("SELECT pid FROM metadata")
        return [item[0] for item in self.cursor.fetchall()]
    
    def get_file_pid_list(self) -> list:
        """
        Get a list of all pids in imageData.
        """
        self.cursor.execute("SELECT pid FROM imageData")
        return [item[0] for item in self.cursor.fetchall()]
        
    def overwrite_tags(self, pid: str, tags: dict) -> None:
        """
        overwrite tags of a picture.
        """
        self.cursor.execute("UPDATE metadata SET tags = ? WHERE pid = ?", (json.dumps(tags), pid))
        self.database.commit()
    
    def add_tags(self, pid: str, tags: dict) -> None:
        """
        Add tags to a picture.
        """
        current_tags = self.get_tags(pid)
        current_tags.update(tags)
        self.overwrite_tags(pid, current_tags)
        
        
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

def collect_data(directory: str) -> None:
    """
    Collects data from a directory and stores it in a database.
    """
    processed_files = 0
    database = PicDatabase()
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            processed_files += 1
            print(f'Processed {processed_files} files', end='\r')

            file_path = os.path.join(root, file)
            if file.endswith(".txt"):
                metadata = parse_metadata(file_path)
                database.insert_metadata(*metadata)
            
            elif file.endswith(".webp"): # ignore webp files because they cannot be processed
                continue

            else:
                image_data = parse_picture(file_path)
                database.insert_image_data(*image_data)
    print("\n")

def merge_dirs(src: str, dst: str) -> None:
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
