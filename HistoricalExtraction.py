import pandas as pd
import Query
import csv


class HistoricalExtraction(object):

    def __init__(self):
        self.CashFlowDB = Query.Query()
        self.CashFlowDB.queryDB("USE test;")

    # Should fill in gaps
    def getData(self, fund):

        self._setupDates(fund)
        minYear = self._getMinYear(fund)
        maxYear = self._getMaxYear(fund)
        minQuarter = self._getMinQuarter(fund)
        maxQuarter = self._getMaxQuarter(fund)

        return self.CashFlowDB.queryDB("""SELECT t1.cfYear, t1.cfQuarter, Market_Value, Distributions, Contributions
FROM (SELECT * FROM dateRange) as t1
LEFT JOIN (SELECT hn.cfYear, hn.cfQuarter, hn.Fund, Market_Value, hd.total AS Distributions, hc.total AS Contributions
        FROM `historicalNav` AS hn 
        LEFT JOIN `historicalDistributions` AS hd
            ON(hn.cfYear = hd.cfYear AND hn.Fund = hd.Fund AND hn.cfQuarter = hd.cfQuarter)
            LEFT JOIN `historicalContributions` AS hc
            ON(hc.cfYear = hn.cfYear AND hc.Fund = hn.Fund AND hc.cfQuarter = hn.cfQuarter)
            WHERE hn.Fund = '{0}'
            ORDER BY hn.Fund, hn.cfYear, hn.cfQuarter) as t2 
ON t1.cfYear = t2.cfYear AND t1.cfQuarter = t2.cfQuarter
WHERE NOT ((t1.cfYear = {1} AND t1.cfQuarter < {3}) OR (t1.cfYear = {2} AND t1.cfQuarter > {4}))
ORDER BY t1.cfYear ASC, t1.cfQuarter ASC;""".format(fund, minYear, maxYear, minQuarter, maxQuarter))



    # Returns the minimum year for a given fund as an integer.
    def _getMinYear(self, fund):
        return self.CashFlowDB.queryDB("""SELECT MIN(hn.cfYear)
FROM `historicalNav` AS hn 
    LEFT JOIN `historicalDistributions` AS hd
        ON(hn.cfYear = hd.cfYear AND hn.Fund = hd.Fund AND hn.cfQuarter = hd.cfQuarter)
        LEFT JOIN `historicalContributions` AS hc
            ON(hc.cfYear = hn.cfYear AND hc.Fund = hn.Fund AND hc.cfQuarter = hn.cfQuarter)
WHERE hn.Fund = '{}'
ORDER BY hn.cfYear ASC, hn.cfQuarter ASC;""".format(fund)).fetchone()[0]

    # Returns the maximum year for a given fund as an integer.
    def _getMaxYear(self, fund):
        return self.CashFlowDB.queryDB("""SELECT MAX(hn.cfYear)
        FROM `historicalNav` AS hn 
            LEFT JOIN `historicalDistributions` AS hd
                ON(hn.cfYear = hd.cfYear AND hn.Fund = hd.Fund AND hn.cfQuarter = hd.cfQuarter)
                LEFT JOIN `historicalContributions` AS hc
                    ON(hc.cfYear = hn.cfYear AND hc.Fund = hn.Fund AND hc.cfQuarter = hn.cfQuarter)
        WHERE hn.Fund = '{}'
        ORDER BY hn.cfYear ASC, hn.cfQuarter ASC;""".format(fund)).fetchone()[0]

    # Returns the starting quarter of the minimum year as an integer.
    def _getMinQuarter(self, fund):
        return self.CashFlowDB.queryDB("""SELECT hn.cfQuarter
        FROM `historicalNav` AS hn 
            LEFT JOIN `historicalDistributions` AS hd
                ON(hn.cfYear = hd.cfYear AND hn.Fund = hd.Fund AND hn.cfQuarter = hd.cfQuarter)
                LEFT JOIN `historicalContributions` AS hc
                    ON(hc.cfYear = hn.cfYear AND hc.Fund = hn.Fund AND hc.cfQuarter = hn.cfQuarter)
        WHERE hn.Fund = '{}'
        ORDER BY hn.cfYear ASC, hn.cfQuarter ASC
        LIMIT 1;""".format(fund)).fetchone()[0]

    # Returns the ending quarter of the maximum year as an integer
    def _getMaxQuarter(self, fund):
        return self.CashFlowDB.queryDB("""SELECT hn.cfQuarter
        FROM `historicalNav` AS hn 
            LEFT JOIN `historicalDistributions` AS hd
                ON(hn.cfYear = hd.cfYear AND hn.Fund = hd.Fund AND hn.cfQuarter = hd.cfQuarter)
                LEFT JOIN `historicalContributions` AS hc
                    ON(hc.cfYear = hn.cfYear AND hc.Fund = hn.Fund AND hc.cfQuarter = hn.cfQuarter)
        WHERE hn.Fund = '{}'
        ORDER BY hn.cfYear DESC, hn.cfQuarter DESC
        LIMIT 1;""".format(fund)).fetchone()[0]

    def writeData(self, fund, fileName):
        print
        a = self.getData(fund)

        #return pd.DataFrame(self.getData())
        modelData = pd.DataFrame(list(a.fetchall()))

        modelData.columns = self._getHeaders(a.description)

        pd.set_option('display.expand_frame_repr', False)

        print "***"
        # Needs bracket for None item
        modelData = modelData.replace([None], 0)
        print "***"
        print modelData

        #with open(fileName, 'a') as file:
        #    modelData.to_csv(file, header=True)

    def _getHeaders(self, description):
        result = []
        for item in description:
            result.append(item[0])
        return result

    def _withinRange(self, firstQuarter, lastQuarter, checkQuarter):
        if checkQuarter[0] > firstQuarter[0] and checkQuarter[0] < lastQuarter[0]:
            return True
        elif checkQuarter[0] == firstQuarter[0] and checkQuarter[1] >= firstQuarter[1]:
            return True
        elif checkQuarter[0] == lastQuarter[0] and checkQuarter[1] < lastQuarter[1]:
            return True
        else:
            return False

    def _createRange(self, firstYear, lastYear):
        # Double for loop through the range of years and 1-4 quarters
        return [(year, quarter) for year in range(firstYear, lastYear + 1) for quarter in range(1, 5)]

    def _setupDates(self, fund):
        minYear = self._getMinYear(fund)
        maxYear = self._getMaxYear(fund)
        self.CashFlowDB.queryDB("DROP TABLE IF EXISTS dateRange;")
        self.CashFlowDB.queryDB("CREATE TABLE dateRange (cfYear int(11), cfQuarter int(11))")
        self.CashFlowDB.queryDB("INSERT INTO dateRange VALUES " + str(self._createRange(minYear, maxYear))[1:-1])
        #return self.CashFlowDB.queryDB("SELECT {}".format(self._createRange(2010, 2015)))




a = HistoricalExtraction()
a.writeData("BC 8", "historicalDataExtraction")
#a._trySelect()
#print a._getMinYear("BC 8")
#print a._getMaxYear("BC 8")
#print a._getMinQuarter("BC 8")
#print a._getMaxQuarter("BC 8")
