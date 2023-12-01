# This file contains objects in the program
# modified picData class to handle more work

class PicData:
    def __init__(self, pid: str, count: int = 1):
        self.source = None
        self.pid = pid
        self.count = count
        self.resolution = {}
        self.size = {}
        self.fileName = {}
        self.directory = ""
        self.liked = False
        self.metadata = False # under this line is the information in metadata(.txt file)
        self.title = ""
        self.user = ""
        self.userId = ""
        self.tags = []
        self.date = ""
        self.description = ""
    
    #lodad functions

    def loadData(self, data: dict):
        self.source = "dict"
        self.pid = data["pid"]
        self.count = data["count"]
        self.resolution = data["resolution"]
        self.size = data["size"]
        self.fileName = data["fileName"]
        self.directory = data["directory"]
        self.liked = data["liked"]
        self.metadata = data["metadata"]
        self.title = data["title"]
        self.user = data["user"]
        self.userId = data["userId"]
        self.tags = data["tags"]
        self.date = data["date"]
        self.description = data["description"]

    #update functions

    def updateToDict(self, data: dict) -> dict:
        """update the data dictionary with the PicData object"""
        if self.source == "dict":
            pass
        else:
            if self.source == "metadata":
                data["metadata"] = self.metadata
                data["title"] = self.title
                data["user"] = self.user
                data["userId"] = self.userId
                data["tags"] = self.tags
                data["date"] = self.date
                data["description"] = self.description
                return data
            else:
                if self.count > data["count"]:
                    data["count"] = self.count
                data["resolution"].update(self.resolution)
                data["size"].update(self.size)
                data["fileName"].update(self.fileName)
                return data

    
    #Adders

    def setSource(self, source: str):
        """Set the source of the PicData object"""
        if source not in ["dict", "metadata", "picture"]:
            print("invalid source")
            return
        self.source = source
    
    def setcount(self,count: int):
        if count > self.count:
            self.count = count

    def addResolution(self, resolution: dict):
        self.resolution.update(resolution)

    def addSize(self, size: dict):
        self.size.update(size)

    def addFileName(self, fileName: dict):
        self.fileName.update(fileName)

    def addDirectory(self, directory: str):
        self.directory = directory

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
        if self.tags is None:
            self.tags = tags
        else:
            self.tags.extend(tags)

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
    
    def getFileName(self):
        return self.fileName

    def getDirectory(self):
        return self.directory

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
        return "https://www.pixiv.net/i/" + self.pid
    
    def toDict(self) -> dict:
        return {
            self.pid:{
                "pid": self.pid,
                "count": self.count,
                "resolution": self.resolution,
                "size": self.size,
                "fileName": self.fileName,
                "directory": self.directory,
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
    def __init__(self, name: str, isTag: bool, parent: list, synonyms: list, subTags: dict, depth: int):
        self.name = name
        self.isTag = isTag
        self.parent = parent
        self.synonyms = synonyms
        self.subTags = subTags
        self.depth = depth

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
    
    def addParentTag(self, parentTag: str) -> None:
        """Add a parent tag to this tag"""
        if parentTag not in self.parent:
            self.parent.append(parentTag)

    def addSubTag(self, SubTag: 'Tag') -> None:
        """Add a sub tag to this tag"""
        name = SubTag.name
        if name not in self.subTags:
            self.subTags[name] = SubTag

    def addSynonym(self, synonym: str) -> None:
        """Add a synonym to this tag"""
        if synonym not in self.synonyms:
            self.synonyms.append(synonym)
    
    def getName(self) -> str:
        """Get the name of the tag"""
        return self.name
    
    def getSubTags(self) -> dict:
        """Get the sub tags of the tag"""
        return self.subTags
    
    def getSynonyms(self) -> list:
        """Get the synonyms of the tag"""
        return self.synonyms
    
class TagTree:
    def __init__(self, tag_data: dict) -> None:
        self.tagDict = {} #a dictionary of all tag objects
        self.root = self.build_tree(tag_data) #the root of the TagTree(is a Tag object)

    def build_tree(self, data: dict, parent=None, depth: int = 0) -> Tag:
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
            subTag = self.build_tree(v, name, depth + 1)
            # Add the new Tag object to the subTags dictionary
            subTags[k] = subTag
        
        #create a new Tag and add it to the tagDict
        newTag = Tag(name, isTag, parent, synonyms, subTags, depth)
        self.tagDict[name] = newTag

        return newTag
    
    def getSubTags(self, tag: str) -> list:
        """USELESS
        Get a list of all subTags of a Tag recursively"""
        if tag not in self.tagDict:
            print("tag not found")
            return None

        subTags = list(self.tagDict[tag].subTags.keys())
        allSubTags = subTags.copy()
        for subTag in subTags:
            allSubTags.extend(self.getSubTags(subTag))

        return allSubTags

    def getAllSubTags(self) -> dict:
        """USELESS
        Get all subtag of tags in the TagTree

        Return a dictionary of all subtags of tags in the TagTree

        use before creating tag index
        """
        subTags = {}
        for tag in self.tagDict:
            subTags[tag] = self.getSubTags(tag)
        return subTags
    
    def getAllParentTag(self, tag: Tag = None, parent: set = None, parent_dict: dict = None, includeSynonyms: bool = False) -> dict:
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

        if tag.isTag:
            # Add the parent tag to the parent set
            parentSet = parent.copy()

            # Add the parent set to the parent_dict
            if tag.name in parent_dict:
                parent_dict[tag.name].update(parentSet)
            else:
                parent_dict[tag.name] = parentSet.copy()

            # Add the parent set to the parent_dict for each synonym
            if includeSynonyms:
                synonyms = tag.getSynonyms()
                for synonym in synonyms:
                    if synonym in parent_dict:
                        parent_dict[synonym].update(parentSet.copy())
                    else:
                        parent_dict[synonym] = parentSet.copy()

            parentSet.add(tag.name)
        else:
            parentSet = parent

        for subTag in tag.subTags.values():
            parent_dict.update(self.getAllParentTag(subTag, parentSet, parent_dict, includeSynonyms))

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
        
        if newTag.getName() in self.tagDict:
            print("newTag already exists")
            return
        
        self.tagDict[newTag.name] = newTag
        self.tagDict[parentTag].addSubTag(newTag)
        self.tagDict[newTag.name].addParentTag(parentTag)
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
        
        self.tagDict[tag].addParentTag(parentTag)
        self.tagDict[parentTag].addSubTag(self.tagDict[tag])
        print(f"added {tag} to {parentTag}")

    def isSubTag(self, tag: str, subTag: str) -> bool:
        """Check if subTag is a sub tag of tag"""
        if tag not in self.tagDict:
            return False

        if subTag in self.tagDict[tag].getSubTags():
            return True

        # Get the sub tags of the tag
        subTags = self.tagDict[tag].getSubTags().keys()

        # Check if subTag is a sub tag of any of the sub tags
        for subTagName in subTags:
            if self.isSubTag(subTagName, subTag):
                return True

        return False