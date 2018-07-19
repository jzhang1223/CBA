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
    useCases = ("Expenses", "Return of Capital", "Subject to Recall", "Income")

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
            i = 1
            for row in sheet:
                i += 1
                self._processRow(row)
                print(str(i) + ":" + str(row))
                #if i >= self.getLimit():
                #    return

    # Skips the first row of the given csv
    def _skipHeader(self, sheet):
        next(sheet)

    def _processRow(self, row):
        # Qtr Evaluation, Initial Commitments, Empty Rows
        if row[0] == "":
            print("Skipped!*** QTR, Commit, Empty Row")
            return
        self._processFund(row)
        if self._isQtr(row):
            self._makeQtr(row)
        elif self._simpleRow(row):
            self._makeSimpleRow(row)
        else: #ignore the base cash flow
            self._makeComplexRow(row)

    # Insert the FundID before adding the row so it will be in the DB. Note: This could potentially add strange fundIDs.
    def _processFund(self, row):
        fundID = row[0]
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO fund VALUES (\"" + fundID + "\")"
                cursor.execute(query)
                connection.commit()
        except Exception as e:
            print e

    def _simpleRow(self, row):
        # If row[2] is has no value or if the other columns(Expenses, ROC, Dist. Sub. to Recall, Income) are all empty
        return row[2] != "" and row[3] == "" and row[4] == "" and row[5] == "" and row[6] == ""

    def _makeSimpleRow(self, row):
        fundID = row[0]
        date = datetime.strptime(row[1], '%m/%d/%y')
        value = row[2]
        typeID =  self._findSimpleTypeID(row)
        notes = row[12]
        result = CashFlow.CashFlow(fundID, date, value, typeID, notes)
        self._processCashFlow(result)

    # Determines if a given row is a Quarter Valuation
    def _isQtr(self, row):
        return row[11] != ""

    # Makes a CashFlow specifically for Quarter Valuations, possibly could be abstracted
    def _makeQtr(self, row):
        fundID = row[0]
        date = datetime.strptime(row[1], '%m/%d/%y')
        value = row[11]
        typeID = self._findNamedType('Balance', 'Quarterly Valuation')
        notes = row[12]
        result = CashFlow.CashFlow(fundID, date, value, typeID, notes)
        self._processCashFlow(result)

    # Tries to add a CashFlow object into the CashFlow table in the DB
    def _processCashFlow(self, cashflow):
        try:
            with connection.cursor() as cursor:
                check = ("SELECT * FROM CashFlow WHERE fundID=\'" + cashflow.getFundID() + "\' AND cfDate=\'" +
                         cashflow.getDate() + "\' AND cashValue=" + cashflow.getValue() + " AND typeID=" +
                         cashflow.getTypeID() + " AND notes=\'" + cashflow.getNotes() + "\'")
                print check
                cursor.execute(check)
                rowHolder = cursor.fetchone()
                if (rowHolder is None):
                    query = ("INSERT INTO CashFlow (fundID, cfDate, cashValue, typeID, notes) " + "VALUES (\'" +
                             cashflow.getFundID() + "\', \'" + cashflow.getDate() + "\', " + cashflow.getValue() + ", " +
                             cashflow.getTypeID() + ", \'" + cashflow.getNotes() + "\')")
                    print '** Adding new CashFlow **'
                    cursor.execute(query)
                    connection.commit()
                else:
                    print '***** CashFlow already exists! *****'
                    return

        except Exception as e:
            print e

    # Looks up the CashFlowType for simple rows
    def _findSimpleTypeID(self, row):
        try:
            with connection.cursor() as cursor:
                result = ""
                useCase = ""
                excelType = row[13].lower()
                cash = int(row[2])
                if "fee" in excelType:
                    result = 'Contribution'
                    useCase = 'Expenses'
                elif "contribution" in excelType or "investment" in excelType or cash < 0:
                    result = 'Contribution'
                    useCase = 'Investment'
                elif "income" in excelType:
                    result = 'Distribution'
                    useCase = 'Income'
                elif "return of capital" in excelType:
                    result = 'Distribution'
                    useCase = 'Return of Capital'
                elif "distribution" in excelType or cash > 0:
                    result = 'Distribution'
                    useCase = 'Standard'
                else:
                    Exception
                #cursor.execute(query)
                #return str(cursor.fetchone()[0])
                return self._findNamedType(result, useCase)
        except Exception as e:
            print e

    # Looks up the typeID specifically for Quarterly Valuation
    def _findQtrType(self):
        try:
            with connection.cursor() as cursor:
                query = ("SELECT typeID FROM CashFlowType "
                         "WHERE result = \'Balance\' AND useCase = \'Quarterly Valuation\'")
                cursor.execute(query)
                return str(cursor.fetchone()[0])
        except Exception as e:
            print e


    def _makeComplexRow(self, row):
        for i in range(3, 7):
            if row[i] != "":
                print "@@ Making Complex Row @@"
                fundID = row[0]
                date = datetime.strptime(row[1], '%m/%d/%y')
                value = row[i]
                temp = self._findResult(row, i)
                typeID = self._findNamedType(temp, self.useCases[i-3])
                notes = row[12]
                result = CashFlow.CashFlow(fundID, date, value, typeID, notes)
                self._processCashFlow(result)

    # Queries the DB for a CashFlowType with given result, useCase
    def _findNamedType(self, result, useCase):
        try:
            with connection.cursor() as cursor:
                query = ("SELECT typeID FROM CashFlowType "
                         "WHERE result = \'" + result + "\' AND useCase = \'" + useCase + "\'")
                cursor.execute(query)
                return str(cursor.fetchone()[0])
        except Exception as e:
            print e

    # Determines whether the element in row[i] should be a contribution or distribution
    def _findResult(self, row, i):
        excelType = row[13]
        notes = row[12]
        if "contribution" in excelType.lower() or "contribution" in notes.lower():
            return "contribution"
        elif "distribution" in excelType.lower() or "distribution" in notes.lower():
            return "distribution"
        # Split up b/c checking in the notes/excel type is a priority
        elif i == 3:
            return "contribution"
        elif i < 7 and i > 3:
            return "distribution"
        else:
            Exception
