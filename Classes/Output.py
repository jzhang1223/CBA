import pandas as pd
import numpy as np
import Query
import CalledPercentage
import CapitalCalled
import CapitalCommited
import Dpi
import Nav
import TotalDistributions
import TotalValue
import Tvpi
import Xirr

class Output(object):

    columnNames = ('Fund', 'Capital Commited', 'Called', 'Called %', 'Distributed', 'NAV', 'Total Value', 'DPI', 'TVPI', 'IRR')
    fundList = None
    fundDF = None

    def __init__(self, date, fundList = None):
        if fundList is None:
            query = Query.Query()
            fundTuples = query.queryDB("SELECT fundID FROM Fund ORDER BY fundID ASC").fetchall()
            self.fundList = self._readFunds(fundTuples)
        else:
            self.fundList = fundList

        self.fundDF = pd.DataFrame(columns = self.columnNames)
        for i in range(len(self.fundList)):
            self.fundDF.loc[i] = self.getRow(self.fundList[i], date)
        print self.fundDF


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


a = Output('18/4/2')
print a.getRow('CCDD062016AF', '18/4/2' )