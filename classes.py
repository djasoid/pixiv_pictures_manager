class PicData:
    def __init__(self, pid, count = 1):
        self.pid = pid
        self.count = count
        self.metadata = False
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
    
    def getMetadata(self):
        return {
            "pid": self.pid,
            "count": self.count,
            "metadata": self.metadata,
            "title": self.title,
            "user": self.user,
            "userId": self.userId,
            "tags": self.tags,
            "date": self.date,
            "description": self.description
        }