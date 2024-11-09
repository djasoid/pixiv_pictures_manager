import json
import sqlite3
import os
import tag_tree as tree
from shutil import copy2
from linecache import getline
from PIL import Image
import dataclasses

def writeJson(data, outputFile: str) -> None:
    """
    Writes data to a JSON file.

    This function takes data, a directory for output, and a filename, then writes the data into a JSON file at the specified location.

    Parameters:
    data: The data to write to the file.
    output_directory (str): The directory to write the file to.
    filename (str): The name of the file to write.
    """
    with open(outputFile, "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def loadJson(filePath: str):
    """
    Loads a JSON file.

    returns data in the JSON file.

    Do not use this function to load tag_tree.json.
    please use loadTagTree() instead.
    """
    with open(filePath, "r", encoding='utf-8') as file:
        data = json.load(file)
    return data

def loadTagTree(tagTreeFile: str = "tag_tree.json") -> tree.TagTree:
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
    tagTree = tree.TagTree(tagTreeDict)
    return tagTree

class PicDatabase:
    def __init__(self):
        self.database = None
        self.cursor = None
        self.loadDatabase()
        
    def loadDatabase(self):
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
    
    def insertImageData(self, pid, num, directory, fileName, fileType, width, height, size):
        """
        Insert image data into the database.
        """
        self.cursor.execute("INSERT OR IGNORE INTO imageData VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (pid, num, directory, fileName, fileType, width, height, size)
                            )
        self.database.commit()
        
    def insertMetadata(
            self, 
            pid, 
            title, 
            tags, 
            description, 
            user, 
            userId, 
            date,
            xRestrict, 
            bookmarkCount=None, 
            likeCount=None, 
            viewCount=None, 
            commentCount=None
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
                userId, 
                date,
                xRestrict, 
                bookmarkCount, 
                likeCount, 
                viewCount, 
                commentCount
            )
        )
        self.database.commit()
    
    def insertTagIndex(self, tag, pids):
        """
        Insert tag index into the database.
        """
        self.cursor.execute("INSERT OR IGNORE INTO tagIndex VALUES (?, ?)", (tag, json.dumps(pids)))
        self.database.commit()
    
    def insertTagIndexDict(self, tagIndexDict: dict[str, list[str]]):
        """
        Insert tag index dictionary into the database.
        """
        for tag, pids in tagIndexDict.items():
            self.insertTagIndex(tag, pids)
        self.database.commit()
    
    def getPidsByTag(self, tag: str) -> set:
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
    
    def getTags(self, pid) -> dict:
        """
        Get tags of a picture.
        """
        self.cursor.execute("SELECT tags FROM metadata WHERE pid = ?", (pid))
        tagsJson = self.cursor.fetchone()
        if tagsJson:
            return json.loads(tagsJson[0])
        else:
            return {}
        
    def getPidList(self) -> list:
        """
        Get a list of all pids in metadata.
        """
        self.cursor.execute("SELECT pid FROM metadata")
        return [item[0] for item in self.cursor.fetchall()]
    
    def getFilePidList(self) -> list:
        """
        Get a list of all pids in imageData.
        """
        self.cursor.execute("SELECT pid FROM imageData")
        return [item[0] for item in self.cursor.fetchall()]
        
    def overwriteTags(self, pid: str, tags: dict) -> None:
        """
        overwrite tags of a picture.
        """
        self.cursor.execute("UPDATE metadata SET tags = ? WHERE pid = ?", (json.dumps(tags), pid))
        self.database.commit()
    
    def addTags(self, pid: str, tags: dict) -> None:
        """
        Add tags to a picture.
        """
        currentTags = self.getTags(pid)
        currentTags.update(tags)
        self.overwriteTags(pid, currentTags)
        
        
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
    tags = {}
    xRestrict = "allAges"
    pid = int(getline(filePath, 2).strip())
    title = getline(filePath, 5).strip()
    user = getline(filePath, 8).strip()
    userId = int(getline(filePath, 11).strip())

    lineNum = 17
    while True: # read tags
        if getline(filePath, lineNum) != "\n":
            tags.update({getline(filePath, lineNum).strip(): "metadata"})
        else:
            if "#R-18" in tags:
                xRestrict = "R-18"
            elif "#R-18G" in tags:
                xRestrict = "R-18G"
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
            description = '\n'.join(descriptionLines)
            return pid, title, tags, description, user, userId, date, xRestrict
        lineNum += 1

def collectData(directory: str) -> None:
    """
    Collects data from a directory and stores it in a database.
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
