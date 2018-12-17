import pandas as pd
from Calculations import CalledPercentage
from Calculations import CapitalCalled
from Calculations import CapitalCommited
from Calculations import Dpi
from Calculations import Nav
from Calculations import TotalDistributions
from Calculations import TotalValue
from Calculations import Tvpi
from Calculations import Xirr
from Classes import Query
pd.set_option("display.max_columns", 10000)

class Output(object):

    columnNames = ('Fund', 'Capital Commited', 'Called', 'Called %', 'Distributed', 'NAV', 'Total Value', 'DPI', 'TVPI', 'IRR')
    fundList = None
    fundDF = None

    def __init__(self, fundList = None):
        if fundList is None:
            query = Query.Query()
            fundTuples = query.queryDB("SELECT fundID FROM Fund ORDER BY fundID ASC").fetchall()
            self.fundList = self._readFunds(fundTuples)
        else:
            self.fundList = fundList

        self.fundDF = pd.DataFrame(columns = self.columnNames)
        self.cashFlowDB = Query.Query()

    # Creates and exports the dataframe, overwrites the info in the file completely.
    def exportOutput(self, fileName, date):
        for i in range(len(self.fundList)):
            # checks only for funds with existing cash flow transactions
            cashFlowCount = self.cashFlowDB.queryDB("SELECT COUNT(*) FROM CashFlow WHERE fundID = '{}'".format(self.fundList[i])).fetchone()[0]
            print cashFlowCount
            if cashFlowCount > 0:
                self.fundDF.loc[i] = self.getRow(self.fundList[i], date)
        print self.fundDF
        self.fundDF.to_csv(fileName, index=False)

    def _getCalledPercentage(self, fundID, date):
        func = CalledPercentage.CalledPercentage()
        return func(fundID, date)

    def _getCapitalCalled(self, fundID, date):
        func = CapitalCalled.CapitalCalled()
        return func(fundID, date)

    def _getCapitalCommited(self, fundID):
        func = CapitalCommited.CapitalCommited()
        return func(fundID)

    def _getDpi(self, fundID, date):
        func = Dpi.Dpi()
        return func(fundID, date)

    def _getGrowth(self, fundID, date):
        pass # real pass

    def _getNav(self, fundID, date):
        func = Nav.Nav()
        return func(fundID, date)

    def _getTotalDistributions(self, fundID, date):
        func = TotalDistributions.TotalDistributions()
        return func(fundID, date)

    def _getTotalValue(self, fundID, date):
        func = TotalValue.TotalValue()
        return func(fundID, date)

    def _getTvpi(self, fundID, date):
        func = Tvpi.Tvpi()
        return func(fundID, date)

    def _getXirr(self, fundID, date):
        func = Xirr.Xirr()
        return func(fundID, date)

    # Returns a list of the stats for a fund on a given date
    def getRow(self, fundID, date):
        result = [fundID, self._getCapitalCommited(fundID), self._getCapitalCalled(fundID, date), self._getCalledPercentage(fundID, date),
                  self._getTotalDistributions(fundID, date), self._getNav(fundID, date), self._getTotalValue(fundID, date),
                  self._getDpi(fundID, date), self._getTvpi(fundID, date), self._getXirr(fundID, date)]
        return result

    # Converts the nested tuples into a list of the fundIDs
    def _readFunds(self, fundTuples):
        result = []
        for tuple in fundTuples:
            result.append(tuple[0])
        return result


tempDate = '18/8/9'
#a = Output("testOutputAverages.csv", tempDate)
#a.exportOutput()
#Output("../testOutput.csv", tempDate)

# Final Output
#Output("RawDataOutput.csv", tempDate)