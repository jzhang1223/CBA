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

    def organizeData(self, fund):
        a = self.getData(fund)

        #return pd.DataFrame(self.getData())
        modelData = pd.DataFrame(list(a.fetchall()))

        modelData.columns = self._getHeaders(a.description)
        modelData.columns.name = fund
        print modelData.columns
        pd.set_option('display.expand_frame_repr', False)

        # Needs bracket for None item
        modelData = modelData.replace([None], 0)
        return modelData

    def writeData(self, modelData, fileName):
        with open(fileName, 'a') as file:
            modelData.to_csv(file, header=True)


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


fileName = "historicalDataExtraction.csv"
df = pd.read_csv("../cbaDBdata/Sample Data Set.csv")
funds = list(set(df["Fund"]))
# Take out the ARBY values
invalidFunds = ["ABRY 5", "ABRY 6", "ABRY 7", "ABRY 8"]
funds = sorted(funds)
for fund in invalidFunds:
    funds.remove(fund)

a = HistoricalExtraction()
allFunds = []
for fund in funds:
    # allFunds....
    #allFunds = pd.join(allFunds, a.organizeData(fund), how='inner')
    #print a.organizeData(fund)
    #print allFunds
    #allFunds = allFunds.join(a.organizeData(fund), how='outer', lsuffix="_first", rsuffix="_next")
    allFunds.append(a.organizeData(fund))
# Changes from list of dataframes to one large dataframe
allFunds = pd.concat(allFunds, ignore_index=True, axis=1)

for i in range(len(allFunds.columns) - 1, -1, -1):
    if not ((i % 5 == 2) or (i % 5 == 3)):
        allFunds = allFunds.drop(i, axis=1)
    elif i % 5 == 2:
        allFunds = allFunds.rename(columns={ allFunds.columns[i]: "Market_Value{}->".format(len(allFunds.columns)-i)})

    elif i % 5 == 3:
        allFunds = allFunds.rename(columns={ allFunds.columns[i]: "<-Distributions{}".format(len(allFunds.columns)-i)})
    else:
        print "*******ERROR******"

print "STARTING"
print allFunds
print "ENDING"

print allFunds.shape[0]

# Number of columns
for i in range(0, allFunds.shape[1], 2):
    # Number of rows
    for j in range(0, allFunds.shape[0]):
        print allFunds.iloc[j,i]
        if allFunds.iloc[j,i] == 0:
            print "TRUE"
            print allFunds.iloc[j,i]
            print allFunds.iloc[j-1][i]
            print "Old, new"
            allFunds.iloc[j,i] = allFunds.iloc[j-1][i]
        #if allFunds[allFunds.columns[0]].iloc[j][i] == 0:
            #allFunds[allFunds.columns[0]].iloc[j][i] = allFunds[allFunds.columns[0]].iloc[j-1][i]
            #print allFunds[allFunds.columns[0]].iloc[j][i]
            #temp = allFunds[allFunds.columns[0]].iloc[j-1][i]
            #allFunds[allFunds.columns[0]].iloc[j][i] = temp
            #print allFunds.iloc[j][i]
        print allFunds.iloc[j,i]



#print allFunds[allFunds.columns[0]].iloc[0][0]
print allFunds
a.writeData(allFunds, fileName)

#a.writeData(allFunds, "historicalDataExtraction.csv", ["Distributions", "Market_Value"])

#a._trySelect()
#print a._getMinYear("BC 8")
#print a._getMaxYear("BC 8")
#print a._getMinQuarter("BC 8")
#print a._getMaxQuarter("BC 8")
