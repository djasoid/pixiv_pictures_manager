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
        self.tagDict = {} #a dictionary of all tags
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

    # path template: ['tag', '全年龄', '角色', '#Fate/GrandOrder']

    def findTag(self, path: list) -> Tag:
        """Find a Tag object in the TagTree using a list of names(like a path)"""
        tag = self.root
        for name in path:
            tag = tag.subTags.get(name)
            if not tag:
                return None
        return tag
    
    def getSubTags(self, path: list) -> list:
        """Get a list of subTags of a Tag object using a list of names(like a path)"""
        tag = self.findTag(path)
        return list(tag.subTags.keys()) if tag else None

    def getAllPath(self, node: Tag = None, path: list =[], path_dict: dict ={}) -> dict:
        """Get all paths in the TagTree"""
        if node is None:
            node = self.root

        # Create a new copy of the path and append the current node's name
        new_path = path + [node.name]

        # If the tag already exists in the dictionary, append the new path
        if node.name in path_dict:
            path_dict[node.name].append(new_path)
        else:
            path_dict[node.name] = [new_path]

        for subTag in node.subTags.values():
            self.getAllPath(subTag, new_path, path_dict)

        return path_dict
    
    def getAllTagPath(self, node: Tag = None, path: list =[], path_dict: dict ={}, includeSynonyms: bool = False) -> dict:
        """Get all tag paths in the TagTree(only include tags), if includeSynonyms is True, add the same path for each synonym"""
        if node is None:
            node = self.root

        # Create a new copy of the path and append the current node's name
        # only if node.isTag is True
        if node.isTag:
            new_path = path + [node.name]
        else:
            new_path = path

        # If the tag already exists in the dictionary, append the new path
        if node.isTag:
            if node.name in path_dict:
                path_dict[node.name].append(new_path)
            else:
                path_dict[node.name] = [new_path]
            # If includeSynonyms is True, add the same path for each synonym
            if includeSynonyms:
                for synonym in node.synonyms:
                    if synonym in path_dict:
                        path_dict[synonym].append(new_path)
                    else:
                        path_dict[synonym] = [new_path]

        for subTag in node.subTags.values():
            self.getAllTagPath(subTag, new_path, path_dict)

        return path_dict

    def addTag(self, path: list, newTag: Tag):
        """Add the new tag to the TagTree at path"""
        tag = self.findTag(path)
        tag.subTags[newTag.name] = newTag

    def getEndTagList(self, tag = None) -> list:
        """
        Get a list of all end tags in the TagTree
        """
        endTagList = []
        if tag == None:
            for tag in self.tagDict.values():
                if not tag.subTags:
                    endTagList.append(tag.name)
        else:
            if not tag.subTags:
                endTagList.append(tag.name)
            else:
                for subTag in tag.subTags.values():
                    endTagList += self.getEndTagList(subTag)
        return endTagList

    def addParentTag(self, subTag: str, parentTag: str) -> None:
        """Add a parent tag to a sub tag, tag must be in the TagTree"""
        if subTag not in self.tagDict:
            print("subTag not found")
            return
        
        if parentTag not in self.tagDict:
            print("parentTag not found")
            return
        
        self.tagDict[subTag].parent.append(parentTag)
        self.tagDict[parentTag].subTags[subTag] = self.tagDict[subTag]
        print(f"added {subTag} to {parentTag}")