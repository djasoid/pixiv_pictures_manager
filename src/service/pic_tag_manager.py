from typing import TYPE_CHECKING

from utils.json import write_json

if TYPE_CHECKING:
    from tag_tree import TagTree
    from database import PicDatabase

class PicTagManager:
    """
    A class that manages picture tags.
    """
    def __init__(self, tag_tree: 'TagTree', pic_database: 'PicDatabase') -> None:
        self.pic_database = pic_database
        self.tag_tree = tag_tree
        self.tag_index_cache = {}
        self.unknown_tags = {}

    def complete_tag(self) -> None:
        """
        iterate through the database and completes tags for each picture data in database with tag tree.
        """
        all_parent_tag_dict = self.tag_tree.get_all_parent_tag(include_synonyms=True)
        pid_list = self.pic_database.get_pid_list()

        for pid in pid_list:
            tags = self.pic_database.get_tags(pid).keys()
            new_tags = set()
            for tag in tags:
                if tag in all_parent_tag_dict:
                    new_tags.update(all_parent_tag_dict[tag])
                else:
                    if tag in self.unknown_tags:
                        self.unknown_tags[tag] += 1
                    else:
                        self.unknown_tags[tag] = 1
            
            new_tags -= tags
            new_tags_dict = {tag: "tree" for tag in new_tags}
            self.pic_database.add_tags(pid, new_tags_dict)

        tags_to_delete = [tag for tag in self.unknown_tags if self.unknown_tags[tag] < 10]
        for tag in tags_to_delete:
            del self.unknown_tags[tag]
            
        sorted_unknown_tags = sorted(self.unknown_tags.items(), key=lambda item: item[1], reverse=True)
        write_json(sorted_unknown_tags, "unknown_tags.json")

    def init_tag_index(self) -> None:
        """
        Initializes a tag index.
        """
        all_parent_tag_dict = self.tag_tree.get_all_parent_tag(include_synonyms=False)
        pid_list = self.pic_database.get_pid_list()

        tag_index: dict[str, list[str]] = {}

        for pid in pid_list:
            tags = self.pic_database.get_tags(pid).keys()
            tag_in_tree = set()
            for tag in tags:
                if tag in all_parent_tag_dict:
                    tag_in_tree.add(tag)
            
            # remove all parent tags from the tag set to remove excessive tags
            tag_set = tag_in_tree.copy()
            for tag in tag_in_tree:
                if tag in tag_set:
                    tag_set -= all_parent_tag_dict[tag]
            
            for tag in tag_set:
                if tag in tag_index:
                    tag_index[tag].append(pid)
                else:
                    tag_index[tag] = [pid]
        
        self.pic_database.insert_tag_index_dict(tag_index)

    def tag_search(self, include_tags: list, exclude_tags: list, include_sub_tags: bool = True) -> set:
        """
        Search for pictures with tags.
        the search will return a set of picture ids that have all the tags in includeTags and none of the tags in excludeTags.
        """
        def find_pids(tag: str) -> set:
            if tag in self.tag_index_cache:
                return self.tag_index_cache[tag]
            else:
                pids = self.pic_database.get_pids_by_tag(tag)
                self.tag_index_cache[tag] = pids
                return pids
        
        all_exclude_tag = exclude_tags.copy()
        all_include_tag = []

        for tag in exclude_tags:
            all_exclude_tag.extend(self.tag_tree.get_sub_tags(tag))
        
        if include_sub_tags:
            for tag in include_tags:
                all_include_tag.append(self.tag_tree.get_sub_tags(tag).append(tag))
                
        include_pid = set()
        for tags in all_include_tag:
            pids = set()
            for tag in tags:
                pids.update(find_pids(tag))
            if include_pid:
                include_pid &= pids
            else:
                include_pid = pids.copy()

        exclude_pid = set()
        for tag in all_exclude_tag:
            exclude_pid.update(find_pids(tag))
        
        return include_pid - exclude_pid
    
if __name__ == "__main__":
    pass