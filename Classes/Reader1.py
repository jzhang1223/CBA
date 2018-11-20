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
        raw_data = raw_data[raw_data["Fund Code"].notna()]
        for row in raw_data.iterrows():
            #self._processRow(row[1])
            print row[1][2]

    def _processRow(self, row):
        # Empty Rows
        if self._isUselessRow(row):
            return
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


    def _isUselessRow(self, row):
        #todo
        return

    def _isSimpleRow(self, row):
        # if there is a cash flow but no other values(Expenses, ROC, Dist. Sub. To Recall, Income)
        return (row.get("Cash Flow") != 0.0 and row.get("Expenses") == 0.0 and row.get("ROC") == 0.0 and
                row.get("Dist. Sub. To Recall") == 0.0 and row.get("Income") == 0.0)



a = Reader("temp")
