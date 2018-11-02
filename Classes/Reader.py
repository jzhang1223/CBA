from APIs import ReaderAPI
from Classes import CashFlow
from datetime import datetime
from Classes import Query
import csv


class Reader(ReaderAPI.ReaderAPI):
    #fileName = None
    #limit = None
    CashFlowDB = Query.Query()
    #count = 0

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
            i = 1
            for row in sheet:
                i += 1
                self._processRow(row)
                print("&& Just Processed ... " + str(i) + ":" + str(row))
                #if i >= self.getLimit():
                #    return

    # Skips the first row of the given csv.
    def _skipHeader(self, sheet):
        next(sheet)

    def _processRow(self, row):
        # Empty Rows
        if self._uselessRow(row):
            return
        if not self._fundExists(row):
            self._processFund(row)
            return
        elif self._isCommitment(row):
            return
        elif self._isQtr(row):
            self._makeQtr(row)
        elif self._simpleRow(row):
            self._makeSimpleRow(row)
        elif self._inferredRow(row):
            #print "*** THIS IS AN INFERRED ROW"
            #self.count += 1
            #print "@@@ COUNT: " + str(self.count)
            self._makeInferredRow(row)
        else:
            # ignore the base cash flow
            self._makeComplexRow(row)

    # Insert the FundID before adding the row so it will be in the DB. Note: This could potentially add strange fundIDs.
    # Also generates the initial commitment value.
    def _processFund(self, row):
        fundID = row[0]
        query = "INSERT INTO fund VALUES (\"" + fundID + "\")"
        self.CashFlowDB.queryDB(query)
        self._makeInitialCommitment(row)

    def _simpleRow(self, row):
        # If row[2] has no value or if the other columns(Expenses, ROC, Dist. Sub. to Recall, Income) are all empty.
        return row[2] != "" and row[3] == "" and row[4] == "" and row[5] == "" and row[6] == ""

    def _makeSimpleRow(self, row):
        fundID = row[0]
        date = datetime.strptime(row[1], '%m/%d/%y')
        value = row[2]
        typeID =  self._findSimpleTypeID(row)
        notes = row[12]
        result = CashFlow.CashFlow(fundID, date, value, typeID, notes)
        self._processCashFlow(result)

    # Determines if a given row is a Quarter Valuation.
    def _isQtr(self, row):
        print row[11]
        return str(row[11]).strip() != ""

    # Makes a CashFlow specifically for Quarter Valuations, possibly could be abstracted.
    def _makeQtr(self, row):
        fundID = row[0]
        date = datetime.strptime(row[1], '%m/%d/%y')
        value = row[11]
        typeID = self._findNamedType('Balance', 'Quarterly Valuation')
        notes = row[12]
        result = CashFlow.CashFlow(fundID, date, value, typeID, notes)
        self._processCashFlow(result)

    # Makes an initial commitment value, should only occur after the fundID is initially inputted.
    # Assumes that initial commitment is the first value of any fund.
    def _makeInitialCommitment(self, row):
        fundID = row[0]
        date = datetime.strptime(row[1], '%m/%d/%y')
        value = row[10]
        typeID = self._findNamedType('Balance', 'Initial Commitment')
        notes = row[12]
        result = CashFlow.CashFlow(fundID, date, value, typeID, notes)
        self._processCashFlow(result)

    # Tries to add a CashFlow object into the CashFlow table in the DB.
    def _processCashFlow(self, cashflow):
        check = ("SELECT * FROM CashFlow WHERE fundID=\'" + cashflow.getFundID() + "\' AND cfDate=\'" +
                         cashflow.getDate() + "\' AND cashValue=" + cashflow.getValue() + " AND typeID=" +
                         cashflow.getTypeID() + " AND notes=\'" + cashflow.getNotes() + "\'")
        cursor = self.CashFlowDB.queryDB(check)
        rowHolder = cursor.fetchone()
        if rowHolder is None:
            query = ("INSERT INTO CashFlow (fundID, cfDate, cashValue, typeID, notes) " + "VALUES (\'" +
                     cashflow.getFundID() + "\', \'" + cashflow.getDate() + "\', " + cashflow.getValue() + ", " +
                     cashflow.getTypeID() + ", \'" + cashflow.getNotes() + "\')")
            self.CashFlowDB.queryDB(query)

    # Looks up the CashFlowType for simple rows.
    def _findSimpleTypeID(self, row):
                result = ""
                useCase = ""
                excelType = row[13].lower()
                cash = int(row[2])
                if "fee" in excelType:
                    result = 'Contribution'
                    useCase = 'Expenses'
                elif "contribution" in excelType or "investment" in excelType:
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
                elif cash < 0:
                    result = 'Contribution'
                    useCase = 'Investment'
                else:
                    return None
                return self._findNamedType(result, useCase)

    # Looks up the typeID specifically for Quarterly Valuation.
    def _findQtrType(self):
        query = ("SELECT typeID FROM CashFlowType "
                 "WHERE result = \'Balance\' AND useCase = \'Quarterly Valuation\'")
        cursor = self.CashFlowDB.queryDB(query)
        return str(cursor.fetchone()[0])

    def _makeComplexRow(self, row):
        useCases = ("Expenses", "Return of Capital", "Subject to Recall", "Income")
        for i in range(3, 7):
            if row[i] != "":
                fundID = row[0]
                date = datetime.strptime(row[1], '%m/%d/%y')
                value = row[i]
                temp = self._findResult(row, i)
                typeID = self._findNamedType(temp, useCases[i-3])
                notes = row[12]
                result = CashFlow.CashFlow(fundID, date, value, typeID, notes)
                self._processCashFlow(result)

    # Queries the DB for a CashFlowType with given result, useCase.
    def _findNamedType(self, result, useCase):
        query = ("SELECT typeID FROM CashFlowType "
                 "WHERE result = \'" + result + "\' AND useCase = \'" + useCase + "\'")
        cursor = self.CashFlowDB.queryDB(query)
        return str(cursor.fetchone()[0])

    # Determines whether the element in row[i] should be a contribution or distribution.
    def _findResult(self, row, i):
        excelType = row[13]
        notes = row[12]
        if "contribution" in excelType.lower() or "contribution" in notes.lower():
            return "contribution"
        elif "distribution" in excelType.lower() or "distribution" in notes.lower():
            return "distribution"
        # Split up b/c checking in the notes/excel type is a priority.
        elif i == 3:
            return "contribution"
        elif i < 7 and i > 3:
            return "distribution"
        else:
            return None

    # Determines if the fund already exists in the database.
    def _fundExists(self, row):
        query = ("SELECT * FROM fund WHERE fundID = \'" + row[0] + "\'")
        cursor = self.CashFlowDB.queryDB(query)
        temp = cursor.fetchone()
        print "***PRINTING FUND LOOKUP"
        print temp
        return temp is not None

    # Determines if a row is useless, usually if it's blank or has $- in certain areas.
    def _uselessRow(self, row):

        fundID = row[0].strip()
        cashFlow = str(row[2].strip())
        commitment = str(row[10].strip())
        qtr = str(row[11].strip())

        noFundID = fundID == ""
        noCashFlow =   (cashFlow == "" or "$-" in cashFlow)
        noCommitment = (commitment == "" or "$-" in commitment)
        noQtr =        (qtr == "" or "$-" in qtr)
        #print "&&& Values: " + row[0] + ":" + row[2] + ":" + row[9] + ":" + row[10]
        #print "@@@ Useful? " + str(noFundID) + " " + str(noCashFlow) + " " + str(noCommitment) + " " + str(noQtr) + "@@@"
        return noFundID or (noCashFlow and noQtr and noCommitment)

    # Determines if a given row is an initial commitment value.
    def _isCommitment(self, row):
        cashFlow = str(row[2].strip())
        commitment = str(row[10].strip())
        qtr = str(row[11].strip())

        noCashFlow = (cashFlow == "" or "$-" in cashFlow)
        hasCommitment = commitment != ""
        noQtr = (qtr == "" or "$-" in qtr)
        #print "@@@ isCommitment?..."
        #print noCashFlow
        #print commitment
        #print hasCommitment
        return noCashFlow and hasCommitment and noQtr

    # Determines if a given row has inferred values.
    def _inferredRow(self, row):
        # Reading in the items and converting them to valid integers
        cashFlow = int(str(row[2].strip()))
        expenses = str(row[3].strip())
        roc = str(row[4].strip())
        income = str(row[6].strip())

        expenses = int(expenses or 0)
        roc = int(roc or 0)
        income = int(income or 0)

        # Separated for readability
        if expenses != 0 and expenses != cashFlow:
            print "PASSED FIRST"
            return True
        if roc != 0 and ((income != 0 and roc + income != cashFlow) or (roc != cashFlow and income == 0)):
            print "PASSED SECOND"
            return True

        else:
            return False


    def _makeInferredRow(self, row):
        cashFlow = int(str(row[2].strip()))
        expenses = str(row[3].strip())
        roc = str(row[4].strip())
        income = str(row[6].strip())

        expenses = int(expenses or 0)
        roc = int(roc or 0)
        income = int(income or 0)
        net = cashFlow
        otherValue = None
        typeID = None

        if expenses == 0:
            net -= roc
            otherValue = roc
            temp = self._findResult(row, 4)
            typeID = self._findNamedType(temp, "Return of Capital")
        elif roc == 0:
            net -= expenses
            otherValue = expenses
            temp = self._findResult(row, 3)
            typeID = self._findNamedType(temp, "Expenses")
        else:
            raise ValueError("Invalid data for inferred row")

        fundID = row[0]
        date = datetime.strptime(row[1], '%m/%d/%y')
        net = str(net)
        otherValue = str(otherValue)
        notes = row[12]
        netRow = CashFlow.CashFlow(fundID, date, net, typeID, notes)
        otherRow = CashFlow.CashFlow(fundID, date, otherValue, typeID, notes)
        self._processCashFlow(netRow)
        self._processCashFlow(otherRow)



