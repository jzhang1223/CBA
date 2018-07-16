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
            i = 0
            for row in sheet:
                i += 1
                self._process(row)
                print(row)
                if i >= self.getLimit():
                    break

    # Skips the first row of the given csv
    def _skipHeader(self, sheet):
        next(sheet)

    def _process(self, row):
        if self._simpleRow(row):
            print # todo
        else: #ignore the base cash flow
            print # todo

    def _simpleRow(self, row):
        # If row[2] is has no value or if the other columns(Expenses, ROC, Dist. Sub. to Recall, Income) are all empty
        if (row[2] == '$-' or row[2] == "" or (row[3] == "" and row[4] == "" and row[5] == "" and row[6] == "")):
            return True



reader1 = Reader("../cbaCashFlowModel.csv", 5);



