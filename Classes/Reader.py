from APIs import ReaderAPI
from Classes import CashFlowType
from Classes import CashFlow
from datetime import datetime
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
        #connection.close()

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
        # Qtr Evaluation
        if row[2] == "" or row[2] == "$-":
            print("Skipped!")
            return
        self._processFund(row)
        if self._simpleRow(row):
            self._makeSimpleRow(row)
        else: #ignore the base cash flow
            print "not simple" # todo

    def _processFund(self, row):
        fundID = row[0]
        # try to send an insert query
        try:
            with connection.cursor() as cursor:
                # Insert the fundID
                query = "INSERT INTO fund VALUES (\"" + fundID + "\")"
                cursor.execute(query)
                connection.commit()
        except Exception as e:
            print e

    # Send a given cashFlow to the database
    def _processCashFlow(self, cashflow):
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO CashFlow (fundID, cfDate, cashValue, typeID, notes) " + "VALUES (\'" + cashflow.getFundID() \
                        + "\', \'" + cashflow.getDate() + "\', " + cashflow.getValue() + ", " + cashflow.getTypeID() \
                        + ", \'" + cashflow.getNotes() + "\')"
                print query
                cursor.execute(query)
                connection.commit()
        except Exception as e:
            print e

    def _simpleRow(self, row):
        # If row[2] is has no value or if the other columns(Expenses, ROC, Dist. Sub. to Recall, Income) are all empty
        return (row[2] == '$-' or row[2] == "" or (row[3] == "" and row[4] == "" and row[5] == "" and row[6] == ""))

    def _makeSimpleRow(self, row):
        fundID = row[0]
        date = datetime.strptime(row[1], '%m/%d/%y')
        value = row[2]
        typeID =  self._findSimpleTypeID(row)
        notes = row[12]
        result = CashFlow.CashFlow(fundID, date, value, typeID, notes)
        self._processCashFlow(result)

    def _findSimpleTypeID(self, row):
            try:
                with connection.cursor() as cursor:
                    query = ""
                    if "fee" in row[13]:
                        query = "SELECT typeID FROM CashFlowType " \
                                "WHERE result = \'Distribution\' AND useCase = \'Expenses\'"

                    elif "contribution" in row[13] or "investment" in row[13] or row[2] < 0:
                        query = "SELECT typeID FROM CashFlowType " \
                                "WHERE result = \'Contribution\' AND useCase = \'Investment\'"

                    elif "return of capital" in row [13]:
                        query = "SELECT typeID FROM CashFlowType " \
                                "WHERE result = \'Distribution\' AND useCase = \'Return of Capital\'"

                    elif "distribution" in row[13] or row[2] > 0:
                        query = "SELECT typeID FROM CashFlowType " \
                                "WHERE result = \'Distribution\' AND useCase = \'Standard\'"

                    else:
                        Exception

                    cursor.execute(query)
                    return str(cursor.fetchone()[0])

            except Exception as e:
                print e





reader1 = Reader("../cbaCashFlowModel.csv", 5);



