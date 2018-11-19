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
        return "~/Box Sync/Shared/Lock-up Fund Client Holdings & Performance Tracker/Cash Flow Model/CBA Cash Flow Model - v2.16.xlsx"

    def getLimit(self):
        raise NotImplementedError("Not necessary to implement")

    def _read(self):
        #todo

        for row in pd.read_excel(ospath(self.getFileName()), sheet_name="Raw_Data", header=1).head(10).iterrows():
            print row[1]


a = Reader("temp")
