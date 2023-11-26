# This file contains all classes will be used in the program
# updated tag management system

class PicData:
    def __init__(self, pid: int, count = 1):
        self.pid = pid
        self.count = count
        self.resolution = {}
        self.size = {}
        self.fileType = None
        self.path = None
        self.liked = False
        self.metadata = False # under this line is the information in metadata(.txt file)
        self.title = None
        self.user = None
        self.userId = None
        self.tags = None
        self.date = None
        self.description = None

    #Adders

    def setcount(self,count: int):
        if count > self.count:
            self.count = count

    def addResolution(self, resolution: dict):
        self.resolution.update(resolution)

    def addSize(self, size: dict):
        self.size.update(size)

    def addType(self, fileType: str):
        self.fileType = fileType

    def addPath(self, path: str):
        self.path = path

    def setLiked(self):
        self.liked = True

    def addMetadata(self):
        self.metadata = True

    def addTitle(self, title):
        self.title = title

    def addUser(self, user):
        self.user = user

    def addUserId(self, userId):
        self.userId = userId

    def addTags(self, tags):
        self.tags = tags

    def addDate(self, date):
        self.date = date

    def addDescription(self, description):
        self.description = description
    
    #Getters

    def getPid(self):
        return self.pid
    
    def getCount(self):
        return self.count
        
    def getResolution(self):
        return self.resolution
    
    def getSize(self):
        return self.size
    
    def getType(self):
        return self.fileType

    def getPath(self):
        return self.path

    def getLiked(self):
        return self.liked
    
    def isMetadataExist(self):
        return self.metadata
    
    def getTitle(self):
        return self.title
    
    def getUser(self):
        return self.user
    
    def getUserId(self):
        return self.userId
    
    def getTags(self):
        return self.tags
    
    def getDate(self):
        return self.date
    
    def getDescription(self):
        return self.description
    
    def getUrl(self):
        return "https://www.pixiv.net/i/" + str(self.pid)
    
    def getMetadata(self) -> dict:
        return {
            str(self.pid):{
                "pid": self.pid,
                "count": self.count,
                "resolution": self.resolution,
                "size": self.size,
                "fileType": self.fileType,
                "path": self.path,
                "liked": self.liked,
                "metadata": self.metadata,
                "title": self.title,
                "user": self.user,
                "userId": self.userId,
                "tags": self.tags,
                "date": self.date,
                "description": self.description
                }
        }

class Tag:
    def __init__(self, name: str, isTag: bool, parent: list, synonyms: list, subTags: dict):
        self.name = name
        self.isTag = isTag
        self.parent = parent
        self.synonyms = synonyms
        self.subTags = subTags

    def to_dict(self) -> dict:
        """Convert the Tag object to a dictionary"""
        subTags_dict = {}
        for k, v in self.subTags.items():
            subTags_dict[k] = v.to_dict()

        return {
            'name': self.name,
            'isTag': self.isTag,
            'parent': self.parent,
            'synonyms': self.synonyms,
            'subTags': subTags_dict
        }

class TagTree:
    def __init__(self, tag_data: dict) -> None:
        self.tagDict = {} #a dictionary of all tag opjects
        self.root = self.build_tree(tag_data) #the root of the TagTree(is a Tag object)

    def build_tree(self, data: dict, parent=None) -> Tag:
        """Build a Tag object from the data dictionary"""
        name = data['name']
        isTag = data['isTag']
        parent = data['parent']
        synonyms = data['synonyms']

        #check if the tag is already in the tagDict
        if name in self.tagDict:
            return self.tagDict[name]

        # Get the 'subTags' value from the data dictionary
        subTags_data = data['subTags']

        # Initialize an empty dictionary for the subTags
        subTags = {}

        # Iterate over the key-value pairs in the subTags_data dictionary
        for k, v in subTags_data.items():
            # For each key-value pair, build a new Tag object
            subTag = self.build_tree(v, name)
            # Add the new Tag object to the subTags dictionary
            subTags[k] = subTag
        
        #create a new Tag and add it to the tagDict
        newTag = Tag(name, isTag, parent, synonyms, subTags)
        self.tagDict[name] = newTag

        return newTag
    
    def getSubTags(self, tag: str) -> list:
        """Get a list of all subTags of a Tag recursively"""
        if tag not in self.tagDict:
            print("tag not found")
            return None

        subTags = list(self.tagDict[tag].subTags.keys())
        allSubTags = subTags.copy()
        for subTag in subTags:
            allSubTags.extend(self.getSubTags(subTag))

        return allSubTags

    def getAllSubTags(self) -> dict:
        """
        Get all subtag of tags in the TagTree

        Return a dictionary of all subtags of tags in the TagTree

        use before creating tag index
        """
        subTags = {}
        for tag in self.tagDict:
            subTags[tag] = self.getSubTags(tag)
        return subTags
    
    def getAllParentTag(self, tag: Tag = None, parent: set = set(), parent_dict: dict ={}, includeSynonyms: bool = False) -> dict:
        """Get all parent tags of tags in the TagTree"""
        if tag is None:
            tag = self.root

        if tag.isTag:
            # Add the parent tag to the parent set
            parentSet = parent.copy()

            # Add the parent set to the parent_dict
            if tag.name in parent_dict:
                parent_dict[tag.name].update(parentSet)
            else:
                parent_dict[tag.name] = parentSet

            # Add the parent set to the parent_dict for each synonym
            if includeSynonyms:
                for synonym in tag.synonyms:
                    if synonym in parent_dict:
                        parent_dict[synonym].update(parentSet)
                    else:
                        parent_dict[synonym] = parentSet

            parentSet.add(tag.name)
        else:
            parentSet = parent

        for subTag in tag.subTags.values():
            self.getAllParentTag(subTag, parentSet, parent_dict)

        return parent_dict

    def addNewTag(self, parentTag: str, newTag: Tag):
        """
        Add a new tag object to the TagTree at sub tag of parentTag
        parentTag must be in the TagTree
        newTag must not be in the TagTree
        """
        if parentTag not in self.tagDict:
            print("parentTag not found")
            return
        
        if newTag.name in self.tagDict:
            print("newTag already exists")
            return
        
        self.tagDict[newTag.name] = newTag
        self.tagDict[parentTag].subTags[newTag.name] = newTag
        self.tagDict[newTag.name].parent.append(parentTag)
        print(f"added {newTag.name} to {parentTag}")

    def getTagList(self) -> list:
        """
        Get a list of all tags in the TagTree
        """
        tagList = []
        for tag in self.tagDict:
            if self.tagDict[tag].isTag:
                tagList.append(tag)
        return tagList

    def addParentTag(self, tag: str, parentTag: str) -> None:
        """Add a parent tag to a existing tag, tag must be in the TagTree"""
        if tag not in self.tagDict:
            print("subTag not found")
            return
        
        if parentTag not in self.tagDict:
            print("parentTag not found")
            return
        
        self.tagDict[tag].parent.append(parentTag)
        self.tagDict[parentTag].subTags[tag] = self.tagDict[tag]
        print(f"added {tag} to {parentTag}")

    def isSubTag(self, tag: str, subTag: str) -> bool:
        """Check if subTag is a sub tag of tag"""
        if tag not in self.tagDict:
            return False

        if subTag in self.tagDict[tag].subTags:
            return True

        # Get the sub tags of the tag
        subTags = self.tagDict[tag].subTags.keys()

        # Check if subTag is a sub tag of any of the sub tags
        for subTagName in subTags:
            if self.isSubTag(subTagName, subTag):
                return True

        return False