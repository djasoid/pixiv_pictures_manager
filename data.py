import json
import sqlite3
import os
import program_objects as progObjs

# the program will generate four json files to store pic data
# 1. Metadata.json: contains all metadata
# 2. TagIndex.json: contains all tags and pids that contain the tags
# 3. IllustratorIndex.json: contains all illustrators info
# 4. NoMetadata.json: contains all pids without metadata

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
    print (f"write to {outputFile} successfully")

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

def loadTagTree(tagTreeFile: str = "tag_tree.json") -> progObjs.TagTree:
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
    Tree = progObjs.TagTree(tagTreeDict)
    return Tree

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
            self.cursor.execute('''CREATE TABLE imageData (
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
            self.cursor.execute('''CREATE TABLE metadata (
                                pid TEXT, 
                                title TEXT, 
                                tags TEXT,
                                description TEXT,
                                user TEXT,
                                userId INT,
                                date TEXT,
                                bookmarkCount INT,
                                likeCount INT,
                                viewCount INT,
                                commentCount INT,
                                xRestrict TEXT,
                                PRIMARY KEY (pid)
                                )'''
                                )
    
    def insertImageData(self, pid, num, directory, fileName, fileType, width, height, size):
        """
        Insert image data into the database.
        """
        self.cursor.execute("INSERT OR IGNORE INTO imageData VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (pid, num, directory, fileName, fileType, width, height, size)
                            )
        self.database.commit()
        
    def insertMetadata(self, 
                       pid, 
                       title, 
                       tags, 
                       description, 
                       user, 
                       userId, 
                       date, 
                       bookmarkCount = None, 
                       likeCount = None, 
                       viewCount = None, 
                       commentCount = None, 
                       xRestrict = None):
        """
        Insert metadata into the database.
        """
        self.cursor.execute("INSERT OR IGNORE INTO metadata VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                            (pid, 
                             title, 
                             tags, 
                             description, 
                             user, 
                             userId, 
                             date, 
                             bookmarkCount, 
                             likeCount, 
                             viewCount, 
                             commentCount, 
                             xRestrict)
                            )
        self.database.commit()
    
    def closeDatabase(self):
        """
        Close the database.
        """
        self.database.close()