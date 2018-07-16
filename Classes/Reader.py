from APIs import ReaderAPI
import csv
import Processor

class Reader(ReaderAPI.ReaderAPI):
    fileName = None
    limit = None

    def __init__(self, fileName, limit):
        self.fileName = fileName
        self.limit = limit
        self.__process()

    def getFileName(self):
        return self.fileName

    def getLimit(self):
        return self.limit

    def __process(self):

        with open(self.getFileName()) as file:
            sheet = csv.reader(file, delimiter=',')
            self.__skipHeader(sheet)
            for row in sheet:
                #Processor(row)
                print(row)

    # Skips the first row of the given csv
    def __skipHeader(self, sheet):
        next(sheet)

reader1 = Reader("../TestingWorkbook.csv", 5);



