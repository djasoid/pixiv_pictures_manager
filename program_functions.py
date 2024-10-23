import tag_tree as tree
import data as dataFn

class Core:
    def __init__(self,  
                 tagTree: tree.TagTree, 
                 ):
        self.picDatabase = dataFn.PicDatabase()
        self.tagTree = tagTree
        self.tagIndexCache = {}
        

    def completeTag(self) -> None:
        """
        iterate through the database and completes tags for each picture data in database with tag tree.
        """
        allParentTagDict = self.tagTree.getAllParentTag(includeSynonyms=True)
        pidList = self.picDatabase.getPidList()

        for pid in pidList:
            tags = self.picDatabase.getTags(pid).keys()
            newTags = set()
            for tag in tags:
                if tag in allParentTagDict:
                    newTags.update(allParentTagDict[tag])
            
            newTags -= tags
            newtagsDict = {tag: "tree" for tag in newTags}
            self.picDatabase.addTags(pid, newtagsDict)

    def initTagIndex(self) -> None:
        """
        Initializes a tag index.
        """
        allParentTagDict = self.tagTree.getAllParentTag(includeSynonyms=False)
        pidList = self.picDatabase.getPidList()

        tagIndex: dict[str, list[str]] = {}

        # interate every picture info
        for pid in pidList:
            tags = self.picDatabase.getTags(pid).keys()
            tagInTree = set()

            # iterate every tag in the picture, check if the tag is in the tag tree then collect tag in the tag tree
            for tag in tags:
                if tag in allParentTagDict:
                    tagInTree.add(tag)
            
            # remove all parent tags from the tag set to remove excessive tags
            tagSet = tagInTree.copy()
            for tag in tagInTree:
                if tag in tagSet:
                    tagSet -= allParentTagDict[tag]
            
            for tag in tagSet:
                if tag in tagIndex:
                    tagIndex[tag].append(pid)
                else:
                    tagIndex[tag] = [pid]
        
        self.picDatabase.insertTagIndexDict(tagIndex)

        


    def tagSearch(self, includeTags: list, excludeTags: list, includeSubTags: bool = False) -> set:
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
        def findPids(tag: str) -> set:
            if tag in self.tagIndexCache:
                return self.tagIndexCache[tag]
            else:
                pids = self.picDatabase.getPidsByTag(tag)
                self.tagIndexCache[tag] = pids
                return pids
            
        # check if the tag is in the tag tree
        for tag in includeTags:
            if not self.tagTree.isInTree(tag):
                print(f"ERROR: tag {tag} not in tag tree")
                return set()
        for tag in excludeTags:
            if not self.tagTree.isInTree(tag):
                print(f"ERROR: tag {tag} not in tag tree")
                return set()
        
        allExcludeTag = excludeTags.copy()
        allIncludeTag = includeTags.copy()

        for tag in excludeTags:
            allExcludeTag.extend(self.tagTree.getSubTags(tag))
        
        if includeSubTags:
            for tag in includeTags:
                allIncludeTag.extend(self.tagTree.getSubTags(tag))

        # from tag index get all pids that contain the tags
        includePid = set()
        excludePid = set()
        for tag in allIncludeTag:
            includePid.update(findPids(tag))
        for tag in allExcludeTag:
            excludePid.update(findPids(tag))
        
        return includePid - excludePid
    
if __name__ == "__main__":
    pass