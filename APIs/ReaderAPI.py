class ReaderAPI(object):

    def getFileName(self):
        return NotImplementedError("Abstract Class")

    def getLimit(self):
        return NotImplementedError("Abstract Class")

    def getConnection(self):
        return NotImplementedError("Abstract Class")