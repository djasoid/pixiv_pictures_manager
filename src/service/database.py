from dataclasses import dataclass, field
from typing import TYPE_CHECKING
import json
import sqlite3
import os

from utils.parser import parse_metadata, parse_picture, parse_csv
from tools.log import log_execution
if TYPE_CHECKING:
    from tag_tree import TagTree
    from controller.picture_manager import DataCollectThread

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
    
    def get_new_connection(self):
        return sqlite3.connect("pic_data.db")
           
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
                ratio REAL,
                PRIMARY KEY (pid, num)
            )'''
        )
        self.cursor.execute(
            '''CREATE TABLE metadata (
                pid INT, 
                title TEXT, 
                tags TEXT,
                completedTags TEXT,
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
    
    def _insert_image_data(
            self, 
            pid: int, 
            num: int, 
            directory: str, 
            file_name: str, 
            file_type: str, 
            width: int, 
            height: int, 
            size: int,
            ratio: float,
            cursor: sqlite3.Cursor = None
        ) -> None:
        """
        Insert image data into the database.
        """
        if not cursor:
            cursor = self.cursor
            
        cursor.execute(
            "INSERT OR IGNORE INTO imageData VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (pid, num, directory, file_name, file_type, width, height, size, ratio)
        )
        
    def _insert_metadata(
            self, 
            pid: int, 
            title: str, 
            tags: list[str], 
            description: str, 
            user: str, 
            user_id: int, 
            date: str,
            xRestrict: str, 
            bookmark_count: int = None, 
            like_count: int = None, 
            view_count: int = None, 
            comment_count: int = None,
            cursor: sqlite3.Cursor = None
        ):
        """
        Insert metadata into the database.
        """
        if not cursor:
            cursor = self.cursor
        
        cursor.execute(
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
                json.dumps(tags, ensure_ascii=False), 
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
    
    def _update_tag_index(self, tag_index_dict: dict[str, set[int]], cursor: sqlite3.Cursor = None) -> None:
        """
        Insert tag index dictionary into the database.
        """
        if not cursor:
            cursor = self.cursor
            
        existing_tags_set = {i[0] for i in cursor.execute("SELECT tag FROM tagIndex").fetchall()}
        for tag, pids in tag_index_dict.items():
            if tag in existing_tags_set:
                current_pids = self.get_pids_by_tag(tag, cursor=cursor)
                current_pids.update(pids)
                cursor.execute("UPDATE tagIndex SET pids = ? WHERE tag = ?", (json.dumps(list(current_pids), ensure_ascii=False), tag))
            else:
               cursor.execute("INSERT INTO tagIndex (tag, pids) VALUES (?, ?)", (tag, json.dumps(list(pids), ensure_ascii=False)))
    
    def get_pids_without_tags(self, cursor: sqlite3.Cursor = None) -> list[int]:
        """
        Get pids without tags.
        """
        if not cursor:
            cursor = self.cursor
        
        result = set()    
        cursor.execute("SELECT pid FROM metadata WHERE completedTags = '[]'")
        result.update([i[0] for i in cursor.fetchall()])
        cursor.execute("SELECT pid FROM imageData WHERE pid NOT IN (SELECT pid FROM metadata)")
        result.update([i[0] for i in cursor.fetchall()])
        return list(result)
    
    def get_pids_by_tag(self, tag: str, cursor: sqlite3.Cursor = None) -> set[int]:
        """
        Get pids by tag.
        """
        if not cursor:
            cursor = self.cursor
            
        cursor.execute("SELECT pids FROM tagIndex WHERE tag = ?", (tag,))
        pids_json = cursor.fetchone()
        if pids_json and pids_json[0]:
            return set(json.loads(pids_json[0]))
        else:
            return set()
    
    def _get_tags(self, pid: int, cursor: sqlite3.Cursor = None) -> set[str]:
        """
        Get tags of a picture.
        """
        if not cursor:
            cursor = self.cursor
            
        cursor.execute("SELECT tags FROM metadata WHERE pid = ?", (pid,))
        tags_json = cursor.fetchone()
        if tags_json:
            return set(json.loads(tags_json[0]))
        else:
            return set()
    
    def _get_completed_tags(self, pid: int, cursor: sqlite3.Cursor = None) -> set[str]:
        """
        Get completed tags of a picture.
        """
        if not cursor:
            cursor = self.cursor
            
        cursor.execute("SELECT completedTags FROM metadata WHERE pid = ?", (pid,))
        tags_json = cursor.fetchone()
        if tags_json:
            return set(json.loads(tags_json[0]))
        else:
            return set()
        
    def _get_pid_list(self, cursor: sqlite3.Cursor = None) -> list[int]:
        """
        Get a list of all pids in metadata.
        """
        if not cursor:
            cursor = self.cursor
        
        cursor.execute("SELECT pid FROM metadata")
        return [item[0] for item in cursor.fetchall()]
    
    def get_file_pid_list(self, cursor: sqlite3.Cursor = None) -> list[int]:
        """
        Get a list of all pids in imageData.

        Returns:
        list: A list of all pids in imageData.
        """
        if not cursor:
            cursor = self.cursor
            
        cursor.execute("SELECT DISTINCT pid FROM imageData")
        return [item[0] for item in cursor.fetchall()]
        
    def overwrite_tags(self, pid: str, tags: list, cursor: sqlite3.Cursor = None) -> None:
        """
        overwrite tags of a picture.

        This function overwrites the tags of a picture.

        Parameters:
        pid (str): The picture id.
        tags (dict): The tags to overwrite.

        Returns:
        None
        """
        if cursor is None:
            cursor = self.cursor

        cursor.execute("UPDATE metadata SET tags = ? WHERE pid = ?", (json.dumps(tags, ensure_ascii=False), pid))
        
    def overwrite_completed_tags(self, pid: str, tags: list, cursor: sqlite3.Cursor = None) -> None:
        """
        overwrite completed tags of a picture.

        This function overwrites the completed tags of a picture.

        Parameters:
        pid (str): The picture id.
        tags (dict): The tags to overwrite.

        Returns:
        None
        """
        if cursor is None:
            cursor = self.cursor
            
        cursor.execute("UPDATE metadata SET completedTags = ? WHERE pid = ?", (json.dumps(tags, ensure_ascii=False), pid))
    
    def add_tags(self, pid: int, tags: set, connection: sqlite3.Connection = None) -> None:
        """
        Add tags to a picture.

        This function adds tags to a picture. If the tag already exists, it will be overwritten.

        Parameters:
        pid (str): The picture id.
        tags (dict): The tags to add.
        
        Returns:
        None
        """
        if not connection:
            connection = self.database
            
        current_tags = self._get_tags(pid, cursor=connection.cursor())
        current_tags.update(tags)
        self.overwrite_tags(pid, current_tags, cursor=connection.cursor())
        connection.commit()
        
    def add_completed_tags(self, pid: int, tags: set, connection: sqlite3.Connection = None) -> None:
        """
        Add completed tags to a picture.

        This function adds completed tags to a picture. If the tag already exists, it will be overwritten.

        Parameters:
        pid (str): The picture id.
        tags (dict): The tags to add.
        
        Returns:
        None
        """
        if not connection:
            connection = self.database
            
        current_tags = self._get_tags(pid, cursor=connection.cursor())
        current_tags.update(tags)
        self.overwrite_tags(pid, current_tags, cursor=connection.cursor())
        connection.commit()

    def insert_csv_data(
            self,
            pid: int, 
            tags: list[str], 
            tags_transl: list[str], 
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
            cursor: sqlite3.Cursor = None
        ) -> None:
        """
        Insert data from a CSV file into the database.

        This function inserts data from a CSV file into the database. It inserts the metadata and image data into the database.

        Returns:
        None
        """
        if not cursor:
            cursor = self.cursor
            
        tag_pairs = list(zip(tags, tags_transl))
        for tag, tag_transl in tag_pairs:
            cursor.execute("INSERT OR REPLACE INTO tags VALUES (?, ?, ?)", (tag, tag_transl, 0))
        
        tags_list = [tag for tag in tags]
        self._insert_metadata(
            pid,
            title, 
            tags_list, 
            description, 
            user,
            user_id, 
            date, 
            xRestrict, 
            bookmark_count=bookmarks, 
            like_count=like,
            view_count=view,
            comment_count=comment,
            cursor=cursor
        )

    @log_execution(
        "Info", 
        "Collecting data from directroy {args[1]}", 
        "Collected data from directory {args[1]}, used {execution_time} seconds"
    )
    def collect_data(self, directory: str, thread: 'DataCollectThread' = None, connection: sqlite3.Connection = None) -> list[int]:
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
        if not connection:
            connection = self.database
            
        processed_files = 0
        processed_metadata_ids = set()
        for root, dirs, files in os.walk(directory):
            for file in files:
                processed_files += 1
                if thread:
                    thread.status_update.emit(f"处理了 {processed_files} 个文件")

                file_path = os.path.join(root, file)
                if file.endswith(".txt"):
                    metadata = parse_metadata(file_path)
                    processed_metadata_ids.add(metadata[0])
                    self._insert_metadata(*metadata, cursor=connection.cursor())
                    
                elif file.endswith(".csv"):
                    csv_data = parse_csv(file_path)
                    for data in csv_data:
                        processed_metadata_ids.add(data[0])
                        self.insert_csv_data(*data, cursor=connection.cursor())

                elif file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg") or file.endswith(".gif"):
                    image_data = parse_picture(file_path)
                    self._insert_image_data(*image_data, cursor=connection.cursor())
                
                elif file.endswith(".webp"): # ignore webp files because they cannot be processed
                    continue
        
        processed_metadata_ids = list(processed_metadata_ids)
        self.count_tags(cursor=connection.cursor())
        connection.commit()
        return processed_metadata_ids

    def count_tags(self, pid_list: list[int] = None, cursor: sqlite3.Cursor = None) -> None:
        """
        Count the number of appearances of each tag in the metadata.
        """
        if cursor is None:
            cursor = self.cursor

        if pid_list is None:
            update_existing = False
            cursor.execute("UPDATE tags SET appearanceCount = 0")
            cursor.execute("SELECT tags FROM metadata")
            pic_tags = cursor.fetchall()
        else:
            update_existing = True
            for pid in pid_list:
                cursor.execute("SELECT tags FROM metadata WHERE pid = ?", (pid,))
                pic_tags = cursor.fetchall()
        
        tag_count = {}
        
        for tags in pic_tags:
            tags_list = json.loads(tags[0])
            for tag in tags_list:
                if tag in tag_count:
                    tag_count[tag] += 1
                else:
                    tag_count[tag] = 1

        if update_existing:
            for tag, count in tag_count.items():
                cursor.execute("SELECT appearanceCount FROM tags WHERE originalTag = ?", (tag,)).fetchone()
                result = cursor.fetchone()
                if result:
                    current_count = result[0]
                    cursor.execute("UPDATE tags SET appearanceCount = ? WHERE originalTag = ?", (current_count + count, tag))
                else:
                    cursor.execute("INSERT INTO tags (originalTag, appearanceCount) VALUES (?, ?)", (tag, count))
        else:
            for tag, count in tag_count.items():
                cursor.execute("INSERT OR IGNORE INTO tags (originalTag, appearanceCount) VALUES (?, ?)", (tag, count))
                cursor.execute("UPDATE tags SET appearanceCount = ? WHERE originalTag = ?", (count, tag))

    def get_metadata_list(self, pids: list | set[int], cursor: sqlite3.Cursor = None) -> list['PicMetadata']:
        """
        Get metadata of a list of pids.

        This function gets the metadata of a list of pids.

        Parameters:
        pid_list (set): A set of pids.

        Returns:
        list: A list of PicMetadata objects.
        """
        if cursor is None:
            cursor = self.cursor
        metadata_list = []
        for pid in pids:
            cursor.execute("SELECT * FROM metadata WHERE pid = ?", (pid,))
            metadata = self.cursor.fetchone()
            if metadata:
                metadata_list.append(PicMetadata(*metadata))
    
        return metadata_list

    def get_metadata_dict(self, pids: list | set[int]) -> dict[int, 'PicMetadata']:
        """
        Get metadata of a list of pids as a dictionary.

        This function gets the metadata of a list of pids as a dictionary.

        Parameters:
        pid_list (set): A set of pids.

        Returns:
        dict: A dictionary of PicMetadata objects.
        """
        metadata_dict = {}
        for pid in pids:
            self.cursor.execute("SELECT * FROM metadata WHERE pid = ?", (pid,))
            metadata = self.cursor.fetchone()
            if metadata:
                metadata_dict[pid] = PicMetadata(*metadata)
        
        return metadata_dict
    
    def get_file_list(self, pids: list | set[int]) -> list['PicFile']:
        """
        Get file data of a list of pids.

        This function gets the file data of a list of pids.

        Parameters:
        pid_list (list): A list of pids.

        Returns:
        list: A list of PicFile objects.
        """
        file_list = []
        for pid in pids:
            self.cursor.execute("SELECT * FROM imageData WHERE pid = ?", (pid,))
            file_data = self.cursor.fetchall()
            for data in file_data:
                file_list.append(PicFile(*data))
        
        return file_list

    def get_tag_count_list(self, cursor: sqlite3.Cursor = None) -> list[tuple[str, str, int]]:
        """
        Get a list of tag counts.

        This function gets a list of tag counts.

        Returns:
        list: A list of tuples containing the tag, the translated tag, and the count.
        """
        if not cursor:
            cursor = self.cursor
            
        cursor.execute("SELECT * FROM tags")
        return cursor.fetchall()
    
    def complete_tag(self, tag_tree: 'TagTree', pid_list: list[int] = None, connection: sqlite3.Connection = None) -> None:
        """
        iterate through the picture tags and complete the tags with parent tags.
        this function will overwrite the completed tags of the pictures.

        Args:
            pid_list (list[int], optional): a list of picture ids to complete the tags. If None, all picture tags will be completed. Defaults to None.

        Returns:
            None
        """
        if not connection:
            connection = self.database

        all_parent_tag_dict = tag_tree.get_all_parent_tag(include_synonyms=True)

        if pid_list is None:
            pid_list = self._get_pid_list(cursor=connection.cursor())

        for pid in pid_list:
            tags = self._get_tags(pid, cursor=connection.cursor())
            completed_tags = set()
            for tag in tags:
                if tag in all_parent_tag_dict:
                    completed_tags.update(all_parent_tag_dict[tag])
                
                if tag_tree.is_in_tree(tag):
                    completed_tags.add(tag)
            
            self.overwrite_completed_tags(pid, list(completed_tags), cursor=connection.cursor())
        
        connection.commit()

    def init_tag_index(self, tag_tree: 'TagTree', pid_list: list[int] = None, connection: sqlite3.Connection = None) -> None:
        """
        Initializes a tag index.
        """
        if connection is None:
            connection = self.database
        
        all_parent_tag_dict = tag_tree.get_all_parent_tag(include_synonyms=False)
        if pid_list is None:
            pid_list = self._get_pid_list(cursor=connection.cursor())

        tag_index: dict[str, set[int]] = {}

        for pid in pid_list:
            tags = self._get_completed_tags(pid, cursor=connection.cursor())
            
            # remove all parent tags from the tag set to remove excessive tags
            tag_set = tags.copy()
            for tag in tags:
                if tag in tag_set:
                    tag_set -= all_parent_tag_dict[tag]
            
            for tag in tag_set:
                if tag in tag_index:
                    tag_index[tag].add(pid)
                else:
                    tag_index[tag] = {pid}
        
        self._update_tag_index(tag_index, cursor=connection.cursor())
        connection.commit()


@dataclass
class PicMetadata:
    pid: int
    title: str
    tags_json: str
    completed_tags_json: str
    description: str
    user: str
    user_id: int
    date: str
    x_restrict: str
    bookmark_count: int
    like_count: int
    view_count: int
    comment_count: int

    def __post_init__(self):
        self.tags: set[str] = set(json.loads(self.tags_json))
        self.completed_tags: set[str] = set(json.loads(self.completed_tags_json))
        

@dataclass
class PicFile:
    pid: int
    num: int
    directory: str
    file_name: str
    file_type: str
    width: int
    height: int
    size: int
    ratio: float
    