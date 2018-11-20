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

        for row in pd.read_excel(ospath(self.getFileName()), sheet_name="Raw_Data", header=1).head(10).iterrows():
            self._processRow(row[1])

    def _processRow(self, row):
        # Empty Rows
        if self._uselessRow(row):
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


a = Reader("temp")
