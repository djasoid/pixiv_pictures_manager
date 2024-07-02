import program_objects as progObjs

"""
Notes, ignore this

initializing
    >>read config file

get metadata dict from pictures
    >>input picture path
    metadataDict = getAllData()
    illustratorInfo = getIllustratorInfo()
    noMetadata = getNoMetadata()
    <<output illustratorInfo, noMetadata

load tagtree
    >>read tagTree.json
    tagTree = initTagTree()
    allParentTagDict = tagTree.getAllParentTag()

complete tag
    >>input metadataDict, allParentTagDict
    metadataDict = completeTag(metadataDict, allParentTagDict) #not implemented yet
    <<output metadataDict

get tag index
    tagIndex = initTagIndex(metadataDict, allParentTagDict)
    <<output tagIndex

initialize complete
    ***picDataPath = ***
    ***picFilePath = ***
    <<write config file
"""

class Core:
    def __init__(self, 
                 metadataDict: "dict[str, any]", 
                 tagTree: progObjs.TagTree, 
                 tagIndex: "dict[str, list[str]]" = None, 
                 illustratorInfo: dict = None, 
                 noMetadata: dict = None
                 ):
        self.metadataDict = metadataDict
        self.tagTree = tagTree
        self.tagIndex = tagIndex
        self.illustratorInfo = illustratorInfo
        self.noMetadata = noMetadata
        self.allParentTagDict = None
        self.unknowTag = set()
        self.tagCount = {}
    
    def genVarForInit(self) -> None:
        """
        Generates variables for initializing the program.

        specificly, it generates allParentTagDict, which will be used in completeTag() and initTagIndex()
        """
        self.allParentTagDict = self.tagTree.getAllParentTag(includeSynonyms=True)

    def completeTag(self) -> None:
        """
        Completes tags in metadataDict.

        This function takes a metadata dictionary and completes the tags in the dictionary.
        """
        if self.allParentTagDict is None:
            self.genVarForInit()

        for pid in self.metadataDict:
            data = self.metadataDict[pid]
            if data["metadata"] != False:
                tags = data["tags"]
                newTags = set()
                for tag in tags:
                    newTags.add(tag)
                    if tag in self.allParentTagDict:
                        newTags.update(self.allParentTagDict[tag])
                    else:
                        self.unknowTag.add(tag)
                    
                    if tag.endswith("users入り"): # not count users入り tag
                        continue
                    
                    if tag in self.tagCount:
                        self.tagCount[tag] += 1
                    else:
                        self.tagCount[tag] = 1
                        
                self.metadataDict[pid]["tags"] = list(newTags)

    def initTagIndex(self) -> "dict[str, list[str]]":
        """
        Initializes a tag index from a metadata dictionary and a parent tag dictionary.
        
        use after completeTag()

        This function uses a metadata dictionary and a parent tag dictionary to initialize a tag index. 
        The tag index is a dictionary where the key is a tag and the value is a list of pids that contain the tag.

        Returns:
        dict: A tag index dictionary.
        """
        if self.allParentTagDict is None:
            self.genVarForInit()

        tagIndex: dict[str, list[str]] = {}

        # interate every picture info
        for pid in self.metadataDict:
            data = self.metadataDict[pid]
            if data["metadata"] != False:
                tags = data["tags"]
                tagInTree = set()

                # iterate every tag in the picture, check if the tag is in the tag tree then collect tag in the tag tree
                for tag in tags:
                    if tag in self.allParentTagDict:
                        tagInTree.add(tag)
                
                # remove all parent tags from the tag set to remove excessive tags
                tagSet = tagInTree.copy()
                for tag in tagInTree:
                    if tag in tagSet:
                        tagSet -= self.allParentTagDict[tag]
                
                for tag in tagSet:
                    if tag in tagIndex:
                        tagIndex[tag].append(pid)
                    else:
                        tagIndex[tag] = [pid]

        return tagIndex

    def tagSearch(self, includeTag: list, excludeTag: list, includeSubTags: bool = False) -> set:
        """
        Searches for tags in a tag index and returns a list of pids.

        This function takes in a tag index, and two lists of tags. It then searches for the tags in the tag index and returns a list of pids that contain the tags.

        Parameters:
        includeTag (list): A list of tags to include.
        excludeTag (list): A list of tags to exclude.
        includeSubTags (bool, optional): Whether to include subtags of the tags in includeTag. Defaults to False.

        Returns:
        set: A set of pids that contain the tags.
        """
        # check if tagIndex is initialized
        if self.tagIndex is None:
            print("ERROR: tagIndex not exist")
            return None

        # check if the tag is in the tag tree
        for tag in includeTag:
            if not self.tagTree.isInTree(tag):
                print(f"ERROR: tag {tag} not in tag tree")
                return None
        for tag in excludeTag:
            if not self.tagTree.isInTree(tag):
                print(f"ERROR: tag {tag} not in tag tree")
                return None
        
        allExcludeTag = []
        allIncludeTag = includeTag.copy()

        for tag in excludeTag:
            allExcludeTag.extend(self.tagTree.getSubTags(tag))
        
        if includeSubTags:
            for tag in includeTag:
                allIncludeTag.extend(self.tagTree.getSubTags(tag))

        # from tag index get all pids that contain the tags
        includePid = set()
        excludePid = set()
        for tag in allIncludeTag:
            includePid.update(self.tagIndex[tag])
        for tag in allExcludeTag:
            excludePid.update(self.tagIndex[tag])
        
        return includePid - excludePid

    def getIllustratorInfo(self) -> dict:
        """
        Returns a dictionary with illustrator info (id, name, pidList).

        This function returns a dictionary with illustrator info (id, name, pidList).

        Returns:
        dict: A dictionary with illustrator info (id, name, pidList).
        """
        illustratorDict = {}
        for pid in self.metadataDict:# iterate every picture info
            data = self.metadataDict[pid]
            if data["metadata"] != False:
                uid = data["userId"]
                if uid in illustratorDict:# check if the illustrator is already in the dictionary
                    if data["user"] not in illustratorDict[uid]["name"]:# check if the name is already in the dictionary
                        illustratorDict[uid]["name"].append(data["user"])# add name to the dictionary
                    illustratorDict[uid]["pidList"].append(data["pid"])# add pid to the dictionary
                else:# illustrator not in the dictionary
                    illustratorDict.update({uid: {"uid": data["userId"], "name":[data["user"]], "pidList":[data["pid"]]}})
        return illustratorDict

    def getNoMetadata(self) -> list:
        """
        Returns a list of pids with no metadata.

        This function returns a list of pids with no metadata.

        Returns:
        list: A list of pids with no metadata.
        """
        noMetadata = []
        for pid in self.metadataDict:# iterate every picture info
            data = self.metadataDict[pid]
            if data["metadata"] == False:
                noMetadata.append(pid)
        return noMetadata

    def isR18(self, metadata: dict) -> bool:
        """
        Checks if a picture contains the R18 tag.

        This function takes a dictionary of picture information and checks if it contains the R18 tag. If it does, it returns True, otherwise it returns False.

        Parameters:
        metadata (dict): A dictionary containing picture information.

        Returns:
        bool: True if the picture contains the R18 tag, False otherwise.
        """
        for tag in metadata["tags"]:
            if tag == "#R-18":
                return True
        return False

    def getTagCount(self) -> tuple:
        """
        Counts the number of times each tag appears in metadataDict.

        This function accepts a dictionary of metadata and extracts all the tags present in the file. It then counts the number of times each tag appears and returns a tuple with two dictionaries. The first dictionary contains all ages tags and the second dictionary contains R-18 tags. In the dictionary, the tag is the key and the number of times it appears is the value.

        Parameters:
        metadataDict (dict): A dictionary of metadata.

        Returns:
        tuple: A tuple containing two dictionaries. The first dictionary contains all ages tags and the second dictionary contains R-18 tags.
        """
        tags = {}
        r18tags = {}
        r18pid = []

        # iterate every picture handle all ages tags 
        for pid in self.metadataDict:
            data = self.metadataDict[pid]
            # check it has metadata or not
            if data["metadata"] != False:
                if self.isR18(data):# check if it is R18
                    r18pid.append(data["pid"])# add pid to r18pid list
                else:# not R18
                    for tag in data["tags"]:
                        if tag in tags:
                            tags[tag] += 1
                        else:
                            tags[tag] = 1

        # handle R18 tags
        for pid in r18pid:# iterate every R18 picture
            pid = str(pid)
            for tag in self.metadataDict[pid]["tags"]:# iterate every tag in the picture
                if tag in tags:# check if the tag is already in tags
                    pass
                else:
                    if tag in r18tags:
                        r18tags[tag] += 1
                    else:
                        r18tags[tag] = 1
        return (tags, r18tags)

    def sortTags(self, tags: dict) -> tuple:
        """
        Sorts a dictionary of tags and returns a sorted tuple.

        This function takes a dictionary of tags and returns a sorted tuple where each element is a dictionary of a tag and its count. The tuple is sorted in decreasing order of count.

        Parameters:
        tags (dict): A dictionary of tags.

        Returns:
        tuple: A sorted tuple where each element is a dictionary of a tag and its count.
        """
        sortedTags = sorted(tags.items(), key=lambda x: x[1], reverse=True)
        return sortedTags
    
    def updateMetadata(self, newData) -> None:
        """
        Updates a metadata dictionary with new data.

        This function a dictionary of new data, and updates the metadata dictionary with the new data.
        """
        for pid in newData:
            if pid not in self.metadataDict:
                self.metadataDict.update({pid: newData[pid]})

    def getUnknowTag(self) -> list:
        """
        Returns a list of unknown tags.

        This function returns a list of unknown tags.
        """
        return list(self.unknowTag)
    
if __name__ == "__main__":
    pass