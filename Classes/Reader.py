from APIs import ReaderAPI
from Classes import CashFlowType
import csv

import pymysql.cursors


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='cba71118',
                             db='cbaDB')

class Reader(ReaderAPI.ReaderAPI):
    fileName = None
    limit = None

    def __init__(self, fileName, limit):
        self.fileName = fileName
        self.limit = limit
        self._read()
        connection.close()

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
                self._processRow(row)
                print(row)
                if i >= self.getLimit():
                    break

    # Skips the first row of the given csv
    def _skipHeader(self, sheet):
        next(sheet)

    def _processRow(self, row):
        self._processFund(row)
        if self._simpleRow(row):
            result = CashFlowType #todo
        else: #ignore the base cash flow
            print # todo

    def _processFund(self, row):
        fundID = row[0]
        # try to send an insert query
        try:
            with connection.cursor() as cursor:
                # Insert the fundID
                query = "INSERT INTO fund VALUES (\"" + fundID + "\")"
                cursor.execute(query)
                connection.commit()
                print "done!"
        except Exception as e:
            print e


    def _simpleRow(self, row):
        # If row[2] is has no value or if the other columns(Expenses, ROC, Dist. Sub. to Recall, Income) are all empty
        return (row[2] == '$-' or row[2] == "" or (row[3] == "" and row[4] == "" and row[5] == "" and row[6] == ""))




reader1 = Reader("../cbaCashFlowModel.csv", 5);



