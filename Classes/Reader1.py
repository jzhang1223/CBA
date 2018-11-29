from APIs import ReaderAPI
from Classes import CashFlow
from datetime import datetime
from Classes import Query
import pandas as pd
from os.path import expanduser as ospath

class Reader(ReaderAPI.ReaderAPI):
    CashFlowDB = Query.Query()

    def __init__(self, fileName):
        self.fileName = fileName
        self._read()

    def getFileName(self):
        #return self.fileName
        return "~/Box Sync/Shared/Lock-up Fund Client Holdings & Performance Tracker/Cash Flow Model/CBA Cash Flow Model - v2.17 Clearspring Analysis.xlsx"

    def getLimit(self):
        raise NotImplementedError("Not necessary to implement")

    def _read(self):
        #todo
        # Reads the Raw_Data sheet, deletes rows where fund is na, and iterates over the rows
        raw_data = pd.read_excel(ospath(self.getFileName()), sheet_name="Raw_Data", header=1)
        raw_data = raw_data.drop(columns = ['Unnamed: 14', 'Unnamed: 15', 'add XIRR using arrays, and terminal value based on max(date).', 'Unnamed: 17'])
        raw_data = raw_data[raw_data["Fund Code"].notna()]
        print raw_data.columns
        print raw_data
        for row in raw_data.iterrows():
            #self._processRow(row[1])
            print self._isCommitment(row[1])

    def _processRow(self, row):
        # Empty Rows
        if self._isUselessRow(row):
            return
        # Need to run sponsor data table sheet before fund is added...
        elif not self._fundExists(row.get("Fund Code")):
            raise ValueError("No valid fund. Try checking the Sponsor Data Table sheet")
        elif self._isCommitment(row):
            self._makeInitialCommitment(row)
        elif self._isQtr(row):
            self._makeQtr(row)
        elif self._isSimpleRow(row):
            self._makeSimpleRow(row)
        elif self._isInferredRow(row):
            self._makeInferredRow(row)
        else:
            # ignore the base cash flow value and make multiple inputs
            self._makeComplexRow(row)


    # From old code before the data was cleaned... may not be needed
    # Previously checked if fundID did not exists or too many $- in certain areas
    def _isUselessRow(self, row):
        #todo
        return False

    # Determines if the fund already exists in the database.
    #todo test
    def _fundExists(self, row):
        query = "SELECT fundID FROM fund WHERE fundID = \'{}\'".format(row['Fund Code'])
        cursor = self.CashFlowDB.queryDB(query)
        temp = cursor.fetchone()
        print temp
        return temp is not None

    # Determines if a given row is an initial commitment value.
    def _isCommitment(self, row):
        print row[1]
        noCashFlow = (pd.isna(row['Cash Flow']))
        hasCommitment = (pd.notna(row['Commitment']))
        noQtr = (pd.isna(row['Qtr Valuation']))
        return noCashFlow and hasCommitment and noQtr

    # Makes an initial commitment value, should only occur after the fundID is initially read through sponsor data table file.
    def _makeInitialCommitment(self, row):
        fundID = row['FundCode']
        date = row['Date']
        value = row['Commitment']
        typeID = self._findNamedType('Balance', 'Initial Commitment')
        notes = row['Notes']
        result = CashFlow.CashFlow(fundID, date, value, typeID, notes)
        self._processCashFlow(result)

    # Queries the DB for a CashFlowType with given result and useCase.
    # todo possibly need to cast result to str type, was done in previous code
    def _findNamedType(self, result, useCase):
        query = "SELECT typeID FROM CashFlowType WHERE result = \'{}\' AND useCase = \'{}\'".format(result, useCase)
        cursor = self.CashFlowDB.queryDB(query)
        return cursor.fetchone()[0]

    # Tries to add a CashFlow object into the CashFlow table in the DB.
    def _processCashFlow(self, cashflow):
        check = ("SELECT * FROM CashFlow WHERE fundID=\'{}\' AND cfDate=\'{}\' AND cashValue=\'{}\' AND typeID=\'{}\'"
                 " AND notes=\'{}\'".format(cashflow.getFundID(), cashflow.getDate(), cashflow.getValue(),
                                            cashflow.getTypeID(), cashflow.getNotes()))
        cursor = self.CashFlowDB.queryDB(check)
        rowHolder = cursor.fetchone()
        if rowHolder is None:
            query = ("INSERT INTO CashFlow (fundID, cfDate, cashValue, typeID, notes) VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\'".format(
                cashflow.getFundID(), cashflow.getDate(), cashflow.getValue(), cashflow.getTypeID(), cashflow.getNotes()))
            self.CashFlowDB.queryDB(query)

    def _isSimpleRow(self, row):
        # if there is a cash flow but no other values(Expenses, ROC, Dist. Sub. To Recall, Income)
        return (row.get("Cash Flow") != 0.0 and row.get("Expenses") == 0.0 and row.get("ROC") == 0.0 and
                row.get("Dist. Sub. To Recall") == 0.0 and row.get("Income") == 0.0)



a = Reader("temp")
