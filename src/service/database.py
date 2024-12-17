import json
import sqlite3
import os

from utils.parser import parse_metadata, parse_picture, parse_csv
from tools.log import log_execution

class PicDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PicDatabase, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.database = None
            self.cursor = None
            self._load_database()
            self.initialized = True

    def __del__(self):
        if self.database:
            self.database.close()

    @log_execution("Info", "Loading database", "Database loaded")
    def _load_database(self):
        """
        Load the database.
        """
        if os.path.exists("pic_data.db"):
            self.database = sqlite3.connect("pic_data.db")
            self.cursor = self.database.cursor()
        else:
            self.database = sqlite3.connect("pic_data.db")
            self.cursor = self.database.cursor()
            self._initialize_database()
           
    @log_execution("Info", "No existing database found. Creating new database", "Database created") 
    def _initialize_database(self):
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
        self.cursor.execute(
            '''CREATE TABLE tags (
                originalTag TEXT,
                translatedTag TEXT,
                appearanceCount INT,
                PRIMARY KEY (originalTag)
            )'''
        )
        self.cursor.execute('''CREATE INDEX tag ON tagIndex (tag)''')
        self.cursor.execute('''CREATE INDEX dataPid ON metadata (pid)''')
        self.cursor.execute('''CREATE INDEX filePid ON imageData (pid)''')
    
    def insert_image_data(
            self, 
            pid: int, 
            num: int, 
            directory: str, 
            file_name: str, 
            file_type: str, 
            width: int, 
            height: int, 
            size: int
        ) -> None:
        """
        Insert image data into the database.
        """
        self.cursor.execute(
            "INSERT OR IGNORE INTO imageData VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (pid, num, directory, file_name, file_type, width, height, size)
        )
        self.database.commit()
        
    def insert_metadata(
            self, 
            pid: int, 
            title: str, 
            tags: dict, 
            description: str, 
            user: str, 
            user_id: int, 
            date: str,
            xRestrict: str, 
            bookmark_count: int = None, 
            like_count: int = None, 
            view_count: int = None, 
            comment_count: int = None
        ):
        """
        Insert metadata into the database.
        """
        self.cursor.execute(
            """
                INSERT INTO metadata (
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
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(pid) DO UPDATE SET
                title=excluded.title, 
                tags=excluded.tags, 
                description=excluded.description, 
                user=excluded.user, 
                userId=excluded.userId,
                date=excluded.date, 
                xRestrict=excluded.xRestrict, 
                bookmarkCount=excluded.bookmarkCount, 
                likeCount=excluded.likeCount,
                viewCount=excluded.viewCount, 
                commentCount=excluded.commentCount
            """,
            (
                pid, 
                title, 
                json.dumps(tags), 
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
    
    def insert_tag_index(self, tag: str, pids: list[int]):
        """
        Insert tag index into the database.
        """
        self.cursor.execute("INSERT OR IGNORE INTO tagIndex VALUES (?, ?)", (tag, json.dumps(pids)))
        self.database.commit()
    
    def insert_tag_index_dict(self, tag_index_dict: dict[str, list[int]]):
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
        pids_json = self.cursor.fetchone()
        if pids_json:
            return set(json.loads(pids_json[0]))
        else:
            return set()
    
    def get_tags(self, pid: int) -> dict:
        """
        Get tags of a picture.
        """
        self.cursor.execute("SELECT tags FROM metadata WHERE pid = ?", (pid))
        tags_json = self.cursor.fetchone()
        if tags_json:
            return json.loads(tags_json[0])
        else:
            return {}
        
    def get_pid_list(self) -> list[int]:
        """
        Get a list of all pids in metadata.
        """
        self.cursor.execute("SELECT pid FROM metadata")
        return [item[0] for item in self.cursor.fetchall()]
    
    def get_file_pid_list(self) -> list:
        """
        Get a list of all pids in imageData.

        Returns:
        list: A list of all pids in imageData.
        """
        self.cursor.execute("SELECT DISTINCT pid FROM imageData")
        return [item[0] for item in self.cursor.fetchall()]
        
    def overwrite_tags(self, pid: str, tags: dict) -> None:
        """
        overwrite tags of a picture.

        This function overwrites the tags of a picture.

        Parameters:
        pid (str): The picture id.
        tags (dict): The tags to overwrite.

        Returns:
        None
        """
        self.cursor.execute("UPDATE metadata SET tags = ? WHERE pid = ?", (json.dumps(tags), pid))
        self.database.commit()
    
    def add_tags(self, pid: int, tags: dict) -> None:
        """
        Add tags to a picture.

        This function adds tags to a picture. If the tag already exists, it will be overwritten.

        Parameters:
        pid (str): The picture id.
        tags (dict): The tags to add.
        
        Returns:
        None
        """
        current_tags = self.get_tags(pid)
        current_tags.update(tags)
        self.overwrite_tags(pid, current_tags)

    def insert_csv_data(
            self,
            pid: int, 
            tags: list, 
            tags_transl: list, 
            user: str, 
            user_id: int, 
            title: str,
            description: str, 
            bookmarks: int,
            like: int,
            view: int,
            comment: int,
            xRestrict: str, 
            date: str, 
        ) -> None:
        """
        Insert data from a CSV file into the database.

        This function inserts data from a CSV file into the database. It inserts the metadata and image data into the database.

        Returns:
        None
        """
        tag_pairs = list(zip(tags, tags_transl))
        for tag, tag_transl in tag_pairs:
            self.cursor.execute("INSERT OR IGNORE INTO tags VALUES (?, ?, ?)", (tag, tag_transl, 0))
        
        tags_dict = {tag: "metadata" for tag in tags}
        self.insert_metadata(
            pid,
            title, 
            tags_dict, 
            description, 
            user, 
            user_id, 
            date, 
            xRestrict, 
            bookmarks, 
            like, 
            view, 
            comment
        )

    @log_execution(
        "Info", 
        "Collecting data from directroy {args[1]}", 
        "Collected data from directory {args[1]}, used {execution_time} seconds"
    )
    def collect_data(self, directory: str) -> list:
        """
        Collects data from a directory and stores it in a database.

        This function reads all files in a directory and processes them. 
        It reads metadata from .txt files, image data from image files, and CSV data from .csv files. 
        It then stores the data in the database.

        Parameters:
        directory (str): The directory to read data from.

        Returns:
        list: A list containing the metadata ids of the processed files.
        """
        processed_files = 0
        processed_metadata_ids = set()
        for root, dirs, files in os.walk(directory):
            for file in files:
                processed_files += 1
                print(f'Processed {processed_files} files', end='\r')

                file_path = os.path.join(root, file)
                if file.endswith(".txt"):
                    metadata = parse_metadata(file_path)
                    processed_metadata_ids.add(metadata[0])
                    self.insert_metadata(*metadata)
                    
                elif file.endswith(".csv"):
                    csv_data = parse_csv(file_path)
                    for data in csv_data:
                        processed_metadata_ids.add(data[0])
                        self.insert_csv_data(*data)

                elif file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg") or file.endswith(".gif"):
                    image_data = parse_picture(file_path)
                    self.insert_image_data(*image_data)
                
                elif file.endswith(".webp"): # ignore webp files because they cannot be processed
                    continue

        print("\n")
        self.database.commit()
        return list(processed_metadata_ids)

    def count_tags(self):
        """
        Count the number of appearances of each tag in the metadata.
        """
        self.cursor.execute("UPDATE tags SET appearanceCount = 0")
        self.cursor.execute("SELECT tags FROM metadata")
        pic_tags = self.cursor.fetchall()
        
        tag_count = {}
        
        for tags in pic_tags:
            tags = json.loads(tags[0])
            for tag in tags:
                if tags[tag] == "metadata":
                    if tag in tag_count:
                        tag_count[tag] += 1
                    else:
                        tag_count[tag] = 1
        
        for tag, count in tag_count.items():
            self.cursor.execute("UPDATE tags SET appearanceCount = ? WHERE originalTag = ?", (count, tag))
        
        self.database.commit()
