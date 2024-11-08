# This file contains the Tag and TagTree classes, which are used to store and manage the tag tree data

class Tag:
    __slots__ = ["name", "isTag", "parent", "synonyms", "subTags", "enName", "tagType"]
    def __init__(self, 
                 name: str, 
                 parent: list[str] = None, 
                 synonyms: set[str] = None, 
                 subTags: dict[str, 'Tag'] = None, 
                 enName: str = "", 
                 tagType: str = ""
                 ):
        self.name = name
        self.enName = enName
        self.tagType = tagType
        
        if self.name.startswith("#"):
            self.isTag = True
        else:
            self.isTag = False

        if parent is None:
            self.parent = []
        else:
            self.parent = parent

        if synonyms is None:
            self.synonyms = set()
        else:
            self.synonyms = synonyms

        if subTags is None:
            self.subTags = {}
        else:
            self.subTags = subTags

    def toDict(self) -> dict:
        """Convert the Tag object to a json serializable dictionary"""
        subTagList = []
        for k in self.subTags.keys():
            subTagList.append(k)

        return {
            self.name: 
            {
                'name': self.name,
                'enName': self.enName,
                'parent': self.parent,
                'synonyms': list(self.synonyms),
                'subTags': subTagList,
                'type': self.tagType
            }
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
            self.synonyms.add(synonym)
    
    def setEnName(self, enName: str) -> None:
        """Set the enName of this tag"""
        self.enName = enName
    
class TagTree:
    tagDict: dict[str, Tag] #a dictionary of all tag objects

    def __init__(self, tagTreeData: dict[str, Tag], root = "标签") -> None:
        """Initialize the TagTree object from the data in tagTree.json file"""
        self.tagTreeData = tagTreeData #a dictionary of all tag data, only used in the buildTree function
        self.tagDict = {} #a dictionary of all tag objects
        self.root = self.buildTree(tagTreeData[root])

    def buildTree(self, data: dict, parent=None) -> Tag:
        """Build a Tag object from the data dictionary"""
        name = data['name']
        enName = data['enName']
        parent = data['parent']
        synonyms = set(data['synonyms'])
        tagType = data['type']
        
        if name in self.tagDict:
            return self.tagDict[name]

        subTagNames = data['subTags']

        subTags = {}
        for subTagName in subTagNames:
            subTag = self.buildTree(self.tagTreeData[subTagName], name)
            subTags[subTagName] = subTag
        
        newTag = Tag(name, parent, synonyms, subTags, enName, tagType)
        self.tagDict[name] = newTag

        return newTag

    def getSubTags(self, tag: str, includeSynonyoms = False) -> list:
        """
        Get a list of all subTags of a Tag recursively
        """
        if tag not in self.tagDict:
            raise ValueError(f"tag {tag} not found")

        subTags = list(self.tagDict[tag].subTags.keys())
        allSubTags = subTags.copy()

        if includeSynonyoms:
            allSubTags.extend(self.tagDict[tag].synonyms)
        for subTag in subTags:
            allSubTags.extend(self.getSubTags(subTag, includeSynonyoms))

        return allSubTags
    
    def getAllParentTag(self, tag: Tag = None, parent: set = None, parentDict: dict[str, set] = None, includeSynonyms: bool = False) -> dict:
        """
        Get all parent tags of tags in the TagTree

        return: (dict) 
            key: (str) tag name
            value: (set) set of parent tags
        """
        if parentDict is None:
            parentDict = {}
        else:
            parentDict = parentDict.copy()
        
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
            if tag.name in parentDict:
                parentDict[tag.name].update(parentSet)
            else:
                parentDict[tag.name] = parentSet.copy()

            # Add the parent set to the parent_dict for each synonym
            if includeSynonyms:
                for synonym in tag.synonyms:
                    if synonym in parentDict:
                        parentDict[synonym].update(parentSet)
                        parentDict[synonym].add(tag.name) # Synonyms are regarded as sub tags of the tag
                    else:
                        parentDict[synonym] = parentSet.copy()
                        parentDict[synonym].add(tag.name)

            parentSet.add(tag.name)
        else:
            parentSet = parent

        for subTag in tag.subTags.values():
            parentDict.update(self.getAllParentTag(subTag, parentSet, parentDict, includeSynonyms))

        return parentDict

    def addNewTag(self, newTag: str, parentTag: str) -> bool:
        """
        Add a new tag to the TagTree at sub tag of parentTag
        parentTag must be in the TagTree
        newTag must not be in the TagTree
        """
        if parentTag not in self.tagDict:
            raise ValueError(f"parentTag {parentTag} not found")
        
        if newTag in self.tagDict:
            raise ValueError(f"tag {newTag} already exists")
        
        NewTag = Tag(newTag)

        self.tagDict[NewTag.name] = NewTag
        self.tagDict[parentTag].addSubTag(NewTag)
        self.tagDict[NewTag.name].addParentTag(parentTag)
        return True

    def deleteTag(self, tag: str, parentTag: str) -> bool:
        """Delete a tag from a parent tag, tag must be in the TagTree"""
        if tag not in self.tagDict:
            raise ValueError(f"tag {tag} not found")
        
        if parentTag not in self.tagDict:
            raise ValueError(f"parentTag {parentTag} not found")
        
        self.tagDict[parentTag].subTags.pop(tag)
        self.tagDict[tag].parent.remove(parentTag)

        # check if the tag has any parent tag left
        if not self.tagDict[tag].parent:
            self.tagDict.pop(tag)

        return True

    def getTagList(self) -> list:
        """
        Get a list of all tags in the TagTree
        """
        tagList = []
        for tag in self.tagDict:
            if self.tagDict[tag].isTag:
                tagList.append(tag)
                
        return tagList

    def addParentTag(self, tag: str, parentTag: str) -> bool:
        """Add a parent tag to a existing tag, tag must be in the TagTree"""
        if tag not in self.tagDict:
            raise ValueError(f"tag {tag} not found")
        
        if parentTag not in self.tagDict:
            raise ValueError(f"parentTag {parentTag} not found")
        
        self.tagDict[tag].addParentTag(parentTag)
        self.tagDict[parentTag].addSubTag(self.tagDict[tag])
        return True

    def isSubTag(self, tag: str, subTag: str) -> bool:
        """Check if subTag is a sub tag of tag"""
        if tag not in self.tagDict:
            return False

        if subTag in self.tagDict[tag].subTags:
            return True

        subTags = self.tagDict[tag].subTags.keys()
        for subTagName in subTags:
            if self.isSubTag(subTagName, subTag):
                return True

        return False
    
    def toDict(self) -> dict:
        """Convert the TagTree object to a json serializable dictionary"""
        outputDict = {}
        for tag in self.tagDict:
            outputDict.update(self.tagDict[tag].toDict())

        return outputDict
    
    def isInTree(self, tag: str) -> bool:
        """Check if a tag is in the TagTree"""
        return tag in self.tagDict