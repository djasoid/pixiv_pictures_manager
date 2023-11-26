"""
initializing
    >>read config file
    ***initialize = true***

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
    ***initialize = false***
    ***picDataPath = ***
    ***picFilePath = ***
    <<write config file
"""