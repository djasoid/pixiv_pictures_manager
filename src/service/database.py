import json
import sqlite3
import os

from utils.parser import parse_metadata, parse_picture


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
