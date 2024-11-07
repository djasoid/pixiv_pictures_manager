import tag_tree as tree
import data as dataFn

class PicTagManager:
    """
    A class that manages picture tags.
    """
    def __init__(self):
        self.picDatabase = dataFn.PicDatabase()
        self.tagTree = dataFn.loadTagTree()
        self.tagIndexCache = {}
        self.unknownTags = {}

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
                else:
                    if tag in self.unknownTags:
                        self.unknownTags[tag] += 1
                    else:
                        self.unknownTags[tag] = 1
            
            newTags -= tags
            newtagsDict = {tag: "tree" for tag in newTags}
            self.picDatabase.addTags(pid, newtagsDict)

        tagsToDelete = [tag for tag in self.unknownTags if self.unknownTags[tag] < 10]
        for tag in tagsToDelete:
            del self.unknownTags[tag]
            
        sortedUnknownTags = sorted(self.unknownTags.items(), key=lambda item: item[1], reverse=True)
        dataFn.writeJson(sortedUnknownTags, "unknown_tags.json")

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

    def tagSearch(self, includeTags: list, excludeTags: list, includeSubTags: bool = True) -> set:
        """
        Search for pictures with tags.
        the search will return a set of picture ids that have all the tags in includeTags and none of the tags in excludeTags.
        """
        def findPids(tag: str) -> set:
            if tag in self.tagIndexCache:
                return self.tagIndexCache[tag]
            else:
                pids = self.picDatabase.getPidsByTag(tag)
                self.tagIndexCache[tag] = pids
                return pids
        
        allExcludeTag = excludeTags.copy()
        allIncludeTag = []

        for tag in excludeTags:
            allExcludeTag.extend(self.tagTree.getSubTags(tag))
        
        if includeSubTags:
            for tag in includeTags:
                allIncludeTag.append(self.tagTree.getSubTags(tag).append(tag))
                
        includePid = set()
        for tags in allIncludeTag:
            pids = set()
            for tag in tags:
                pids.update(findPids(tag))
            if includePid:
                includePid &= pids
            else:
                includePid = pids.copy()

        excludePid = set()
        for tag in allExcludeTag:
            excludePid.update(findPids(tag))
        
        return includePid - excludePid
    
if __name__ == "__main__":
    pass