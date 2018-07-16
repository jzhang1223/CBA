from APIs import ReaderAPI
import csv


class Reader(ReaderAPI.ReaderAPI):
    fileName = None
    limit = None

    def __init__(self, fileName, limit):
        self.fileName = fileName
        self.limit = limit
        self._read()

    def getFileName(self):
        return self.fileName

    def getLimit(self):
        return self.limit

    def _read(self):

        with open(self.getFileName()) as file:
            sheet = csv.reader(file, delimiter=',')
            self._skipHeader(sheet)
            for row in sheet:
                self._process(row)
                print(row)

    # Skips the first row of the given csv
    def _skipHeader(self, sheet):
        next(sheet)

    def _process(self, row):
        print 3#

reader1 = Reader("../TestingWorkbook.csv", 5);



