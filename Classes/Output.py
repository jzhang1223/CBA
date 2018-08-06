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

    def __init__(self, fundList = None):
        if fundList is None:
            query = Query.Query()
            self.fundList = query.queryDB("SELECT fundID FROM Fund ORDER BY fundID ASC")
        else:
            self.fundList = fundList

        self.fundDF = pd.DataFrame(columns = self.columnNames, index = range(len(fundList)))


    def _getCalledPercentage(self, fundID, date):
        func = CalledPercentage.CalledPercentage()
        return func(fundID, date)

    def _getCapitalCalled(self, fundID, date):
        func = CapitalCalled.CapitalCalled()
        return func(fundID, date)

    def getCapitalCommited(self, fundID):
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

    def getTotalDistributions(self, fundID, date):
        func = TotalDistributions.TotalDistributions()
        return func(fundID, date)

    def getTotalValue(self, fundID, date):
        func = TotalValue.TotalValue()
        return func(fundID, date)

    def getTvpi(self, fundID, date):
        func = Tvpi.Tvpi()
        return func(fundID, date)

    def getXirr(self, fundID, date):
        func = Xirr.Xirr()
        return func(fundID, date)