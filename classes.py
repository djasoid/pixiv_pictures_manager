# This file contains all classes will be used in the program
class PicData:
    def __init__(self, pid, count = 1):
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

    def setcount(self,count):
        if count > self.count:
            self.count = count

    def addResolution(self, resolution):
        self.resolution.update(resolution)

    def addSize(self, size):
        self.size.update(size)

    def addType(self, fileType):
        self.fileType = fileType

    def addPath(self, path):
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