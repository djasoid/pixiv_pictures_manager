from utils.json import load_json, write_json

class Tag:
    __slots__ = ["name", "is_tag", "parent", "synonyms", "sub_tags", "en_name", "tag_type"]
    def __init__(self, 
                 name: str, 
                 parent: list[str] = None, 
                 synonyms: set[str] = None, 
                 sub_tags: dict[str, 'Tag'] = None, 
                 enName: str = "", 
                 tagType: str = ""
                 ):
        self.name = name
        self.en_name = enName
        self.tag_type = tagType
        
        if self.name.startswith("#"):
            self.is_tag = True
        else:
            self.is_tag = False

        if parent is None:
            self.parent = []
        else:
            self.parent = parent

        if synonyms is None:
            self.synonyms = set()
        else:
            self.synonyms = synonyms

        if sub_tags is None:
            self.sub_tags = {}
        else:
            self.sub_tags = sub_tags

    def to_dict(self) -> dict:
        """Convert the Tag object to a json serializable dictionary"""
        sub_tag_list = []
        for k in self.sub_tags.keys():
            sub_tag_list.append(k)

        return {
            self.name: 
            {
                'name': self.name,
                'enName': self.en_name,
                'parent': self.parent,
                'synonyms': list(self.synonyms),
                'subTags': sub_tag_list,
                'type': self.tag_type
            }
        }
    
    def add_parent_tag(self, parent_tag: str) -> None:
        """Add a parent tag to this tag"""
        if parent_tag not in self.parent:
            self.parent.append(parent_tag)

    def add_sub_tag(self, sub_tag: 'Tag') -> None:
        """Add a sub tag to this tag"""
        name = sub_tag.name
        if name not in self.sub_tags:
            self.sub_tags[name] = sub_tag

    def add_synonym(self, synonym: str) -> None:
        """Add a synonym to this tag"""
        if synonym not in self.synonyms:
            self.synonyms.add(synonym)
    
    def set_en_name(self, enName: str) -> None:
        """Set the enName of this tag"""
        self.en_name = enName

    def remove_synonym(self, synonym: str) -> None:
        """Remove a synonym from this tag"""
        if synonym in self.synonyms:
            self.synonyms.remove(synonym)
    
class TagTree:
    tag_dict: dict[str, Tag] #a dictionary of all tag objects

    def __init__(self, tag_tree_file: str) -> None:
        """Initialize the TagTree object from the data in tagTree.json file"""
        self.tag_dict = {} #a dictionary of all tag objects
        self.file_path = tag_tree_file
        self.load_tag_tree(tag_tree_file)
        
    def build_tree(self, tag_tree_data: dict[str, dict], tag_data: dict[str, str|list], parent=None) -> Tag:
        """Build a Tag object from the data dictionary"""
        name = tag_data['name']
        en_name = tag_data['enName']
        parent = tag_data['parent']
        synonyms = set(tag_data['synonyms'])
        tag_type = tag_data['type']
        
        if name in self.tag_dict:
            return self.tag_dict[name]

        sub_tag_names = tag_data['subTags']

        sub_tags = {}
        for sub_tag_name in sub_tag_names:
            sub_tag = self.build_tree(tag_tree_data, tag_tree_data[sub_tag_name], name)
            sub_tags[sub_tag_name] = sub_tag
        
        new_tag = Tag(name, parent, synonyms, sub_tags, en_name, tag_type)
        self.tag_dict[name] = new_tag

        return new_tag

    def get_sub_tags(self, tag: str, include_synonyoms = False) -> list:
        """
        Get a list of all subTags of a Tag recursively
        """
        if tag not in self.tag_dict:
            raise ValueError(f"tag {tag} not found")

        sub_tags = list(self.tag_dict[tag].sub_tags.keys())
        all_sub_tags = sub_tags.copy()

        if include_synonyoms:
            all_sub_tags.extend(self.tag_dict[tag].synonyms)
        for subTag in sub_tags:
            all_sub_tags.extend(self.get_sub_tags(subTag, include_synonyoms))

        return all_sub_tags
    
    def get_all_parent_tag(
            self, 
            tag: Tag = None, 
            parent: set = None, 
            parent_dict: dict[str, set] = None, 
            include_synonyms: bool = False
        ) -> dict[str, set[str]]:
        """
        Get all parent tags of tags in the TagTree

        return: (dict) 
            key: (str) tag name
            value: (set) set of parent tags
        """
        if parent_dict is None:
            parent_dict = {}
        else:
            parent_dict = parent_dict.copy()
        
        if parent is None:
            parent = set()
        else:
            parent = parent.copy()

        if tag is None:
            tag = self.root

        if not tag.is_tag:
            parent_set = parent
        else:
            # Add the parent tag to the parent set
            parent_set = parent.copy()

            # Add the parent set to the parent_dict
            if tag.name in parent_dict:
                parent_dict[tag.name].update(parent_set)
            else:
                parent_dict[tag.name] = parent_set.copy()

            # Add the parent set to the parent_dict for each synonym
            if include_synonyms:
                for synonym in tag.synonyms:
                    if synonym in parent_dict:
                        parent_dict[synonym].update(parent_set)
                        parent_dict[synonym].add(tag.name) # Synonyms are regarded as sub tags of the tag
                    else:
                        parent_dict[synonym] = parent_set.copy()
                        parent_dict[synonym].add(tag.name)

            parent_set.add(tag.name)

        for sub_tag in tag.sub_tags.values():
            parent_dict.update(self.get_all_parent_tag(sub_tag, parent_set, parent_dict, include_synonyms))

        return parent_dict

    def add_new_tag(self, new_tag: str, parent_tag: str) -> bool:
        """
        Add a new tag to the TagTree at sub tag of parentTag
        parentTag must be in the TagTree
        newTag must not be in the TagTree
        """
        if parent_tag not in self.tag_dict:
            raise KeyError(f"parentTag {parent_tag} not found")
        
        if new_tag in self.tag_dict:
            raise ValueError(f"tag {new_tag} already exists")
        
        new_tag = Tag(new_tag)

        self.tag_dict[new_tag.name] = new_tag
        self.tag_dict[parent_tag].add_sub_tag(new_tag)
        self.tag_dict[new_tag.name].add_parent_tag(parent_tag)
        return True

    def delete_tag(self, tag: str, parent_tag: str) -> bool:
        """Delete a tag from a parent tag, tag must be in the TagTree"""
        if tag not in self.tag_dict:
            raise KeyError(f"tag {tag} not found")
        
        if parent_tag not in self.tag_dict:
            raise KeyError(f"parent tag {parent_tag} not found")
        
        self.tag_dict[parent_tag].sub_tags.pop(tag)
        self.tag_dict[tag].parent.remove(parent_tag)

        return True

    def get_tag_list(self) -> list:
        """
        Get a list of all tags in the TagTree
        """
        tag_list = []
        for tag in self.tag_dict:
            if self.tag_dict[tag].is_tag:
                tag_list.append(tag)
                
        return tag_list

    def add_parent_tag(self, tag: str, parent_tag: str) -> bool:
        """Add a parent tag to a existing tag, tag must be in the TagTree"""
        if tag not in self.tag_dict:
            raise KeyError(f"tag {tag} not found")
        
        if parent_tag not in self.tag_dict:
            raise KeyError(f"parentTag {parent_tag} not found")
        
        self.tag_dict[tag].add_parent_tag(parent_tag)
        self.tag_dict[parent_tag].add_sub_tag(self.tag_dict[tag])
        return True

    def is_sub_tag(self, tag: str, sub_tag: str) -> bool:
        """Check if subTag is a sub tag of tag"""
        if tag not in self.tag_dict:
            return False

        if sub_tag in self.tag_dict[tag].sub_tags:
            return True

        sub_tags = self.tag_dict[tag].sub_tags.keys()
        for sub_tag_name in sub_tags:
            if self.is_sub_tag(sub_tag_name, sub_tag):
                return True

        return False
    
    def to_dict(self) -> dict:
        """Convert the TagTree object to a json serializable dictionary"""
        output_dict = {}
        for tag in self.tag_dict:
            output_dict.update(self.tag_dict[tag].to_dict())

        return output_dict
    
    def is_in_tree(self, tag: str) -> bool:
        """Check if a tag is in the TagTree"""
        return tag in self.tag_dict
    
    def load_tag_tree(self, tag_tree_file: str, root = "标签") -> None:
        """
        Initializes TagTree object from a JSON file.

        Parameters:
        tagTreeFile (str): The JSON file to load.
        """
        tag_tree_data = load_json(tag_tree_file)
        self.root = self.build_tree(tag_tree_data, tag_tree_data[root])
        
    def save_tree(self) -> None:
        """Save the TagTree object to the original file"""
        write_json(self.to_dict(), self.file_path)