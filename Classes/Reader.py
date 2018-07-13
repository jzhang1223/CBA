from APIs import ReaderAPI

class Reader(ReaderAPI.ReaderAPI):
    fileName = None
    limit = None

    def __init__(self, fileName, limit):
        self.fileName = fileName
        self.limit = limit
        self.__process(self)

    def getLimit(self):
        return self.limit

    def __process(self):
        print 3