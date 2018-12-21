import pandas as pd
from os.path import expanduser as ospath
from Classes import Query
from Classes import ValidationTables


class ValidationReader(object):

    def __init__(self, fileName):
        self.CashFlowDB = Query.Query()
        self.fileName = fileName
        #self.filePath = '~/Box Sync/Shared/Lock-up Fund Client Holdings & Performance Tracker/Cash Flow Model/{}.xlsx'.format(fileName)
        self.validationDf = pd.read_excel(ospath(self.fileName), sheet_name='Validation', header=1)

        self.sponsorDataTableDf = pd.read_excel(ospath(self.fileName), sheet_name='Sponsor Data Table', header=1)[["ID Code",
            "Client", "Sponsor", "Fund Family", "Designation", "Fund Style", "Vintage Year", "Close Date",
            "Invest Start Date", "Fund Size ($M)", "Commitment ($M)","Contribution (% of Rem. Commit)", "Unnamed: 14",
            "Unnamed: 15", "Unnamed: 16", "Unnamed: 17", "Model Metrics", "Unnamed: 19", "Unnamed: 20", "Model Years to",
            "Unnamed: 22", "Projected Metrics", "Unnamed: 29", "Unnamed: 30", "Projected Years to", "Unnamed: 32", "Currency",
            "Projected Contribution (% of Rem. Commit)", "Unnamed: 24", "Unnamed: 25", "Unnamed: 26","Unnamed: 27"]]
        print pd.read_excel(ospath(fileName), sheet_name='Sponsor Data Table', header=1).columns

        # Renamming the columns to be readable
        self.sponsorDataTableDf.columns = ["ID Code", "Client", "Sponsor", "Fund Family", "Designation", "Fund Style", "Vintage Year",
            "Close Date", "Invest Start Date", "Fund Size", "Commitment", "Contribution 1", "Contribution 2", "Contribution 3",
            "Contribution 4", "Contribution 5", "Bow", "Growth Rate", "Yield", "Invest Years", "Life", "Projected Bow",
            "Projected Growth", "Projected Yield", "Projected Invest Years", "Projected Life", "Currency", "Projected Contribution 1",
            "Projected Contribution 2", "Projected Contribution 3", "Projected Contribution 4", "Projected Contribution 5"]

        self.sponsorDataTableDf = self.sponsorDataTableDf[self.sponsorDataTableDf["ID Code"].notna()]
        self.sponsorDataTableDf["Fund Family"] = self.sponsorDataTableDf["Fund Family"].str.strip()
        self.sponsorDataTableDf["Fund Size"] = self.sponsorDataTableDf["Fund Size"].fillna(value='null')
        print self.sponsorDataTableDf.head(3)

        # Should probably be abstracted given more time
        self.initializeClientDf()
        self.initializeFundStyleDf()
        self.initializeSponsorDf()
        self.initializeMergedDf()

    # Cleans the sponsor info.
    def initializeSponsorDf(self):
        self.sponsorDf = self.validationDf[['Sponsor_List', 'Sponsor_Code']]
        self.sponsorDf = self.sponsorDf.dropna()
        self.sponsorDf['Sponsor_List'] = self.sponsorDf['Sponsor_List'].str.strip()

    # Cleans the fund style info.
    def initializeFundStyleDf(self):
        self.fundStyleDf = self.validationDf[['Fund_Style', 'Fund_Code']]
        self.fundStyleDf = self.fundStyleDf.dropna()
        self.fundStyleDf['Fund_Style'] = self.fundStyleDf['Fund_Style'].str.strip()

    # Cleans the client info.
    def initializeClientDf(self):
        self.clientDf = self.validationDf[["Client_List", "Client_Code"]]
        self.clientDf = self.clientDf.dropna()
        self.clientDf['Client_List'] = self.clientDf['Client_List'].str.strip()

    # Cleans the merged info of sponsors and families.
    def initializeMergedDf(self):
        self.familyDf = self.sponsorDataTableDf[["Sponsor", "Fund Family"]]
        self.familyDf = self.familyDf.dropna()
        self.familyDf['Sponsor'] = self.familyDf['Sponsor'].str.strip()
        self.familyDf['Fund Family'] = self.familyDf['Fund Family'].str.strip()

        self.mergedDf = pd.merge(self.sponsorDf, self.familyDf, left_on='Sponsor_List', right_on='Sponsor')[
            ['Sponsor_Code', 'Fund Family']]
        self.mergedDf = self.mergedDf.drop_duplicates()

    # Processes and inserts sponsor info.
    def processSponsors(self):
        for row in self.sponsorDf.iterrows():
            rowItem = ValidationTables.Sponsor(row[1].get("Sponsor_Code"), row[1].get("Sponsor_List"))
            check = ("SELECT * FROM Sponsor WHERE sponsorId=\'{}\' AND sponsorName=\'{}\'".format(
                rowItem.getSponsorId().encode('utf-8'), rowItem.getSponsorName().encode('utf-8')))
            if self._rowDoesntExist(check):
                query = ("INSERT INTO Sponsor (sponsorId, sponsorName) VALUES (\'{}\', \'{}\')".format(
                    rowItem.getSponsorId().encode('utf-8'), rowItem.getSponsorName().encode('utf-8')))
                self.CashFlowDB.queryDB(query)

    # Processes and inserts fund style info.
    def processFundStyleDf(self):
        for row in self.fundStyleDf.iterrows():
            rowItem = ValidationTables.FundStyle(row[1].get("Fund_Code"), row[1].get("Fund_Style"))
            check = ("SELECT * FROM FundStyle WHERE fundStyleId=\'{}\' AND fundStyleName=\'{}\'".format(
                rowItem.getFundStyleId().encode('utf-8'), rowItem.getfundStyleName().encode('utf-8')))
            if self._rowDoesntExist(check):
                query = ("INSERT INTO FundStyle (fundStyleId, fundStyleName) VALUES (\'{}\', \'{}\')".format(
                    rowItem.getFundStyleId().encode('utf-8'), rowItem.getfundStyleName().encode('utf-8')))
                self.CashFlowDB.queryDB(query)

    # Processes and inserts client info.
    def processClientDf(self):
        for row in self.clientDf.iterrows():
            rowItem = ValidationTables.FundClient(row[1].get("Client_Code"), row[1].get("Client_List"))
            check = ("SELECT * FROM FundClient WHERE clientId=\'{}\' AND clientName=\'{}\'".format(
                rowItem.getClientId().encode('utf-8'), rowItem.getClientName().encode('utf-8')))
            if self._rowDoesntExist(check):
                query = ("INSERT INTO FundClient (clientId, clientName) VALUES (\'{}\', \'{}\')".format(
                    rowItem.getClientId().encode('utf-8'), rowItem.getClientName().encode('utf-8')))
                self.CashFlowDB.queryDB(query)

    # Processes and inserts family info.
    def processMergedDf(self):
        for row in self.mergedDf.iterrows():
            rowItem = ValidationTables.Family(row[1].get("Fund Family"), row[1].get("Sponsor_Code"))
            check = ("SELECT * FROM Family WHERE familyName=\'{}\' AND sponsorId=\'{}\'".format(
                rowItem.getFamilyName().encode('utf-8'), rowItem.getSponsorId().encode('utf-8')))
            if self._rowDoesntExist(check):
                query = ("INSERT INTO Family (familyName, sponsorId) VALUES (\'{}\', \'{}\')".format(
                    rowItem.getFamilyName().encode('utf-8'), rowItem.getSponsorId().encode('utf-8')))
                self.CashFlowDB.queryDB(query)

    # Processes and inserts fund info. Will update data if parameters are changed.
    def processFundInfo(self):
        fundDataDf = self.sponsorDataTableDf[self.sponsorDataTableDf["ID Code"].notna()]
        for row in fundDataDf.iterrows():
            check = ("SELECT * FROM Fund WHERE fundId=\'{}\'".format(row[1].get("ID Code")))
            if self._rowDoesntExist(check):
                print "ROW DOESNT EXIST"
                self._addFund(row)
                self._appendFund(row)
                print "Adding new row"
            else:
                self._appendFund(row)
                print "Appending to existing row"


    # Adds all statistics to an existing fund that needs more info.
    def _appendFund(self, row):
        row = row[1]
        # FamilyID PK is just the family name so its OK
        fundStyleId = self._findId("FundStyle", "fundStyleId", "fundStyleName", row.get("Fund Style"))
        if pd.isnull(row.get("Client")):
            fundClientId = "null"
        else:
            fundClientId = "\'{}\'".format(self._findId("FundClient", "clientId", "clientName", row.get("Client")))

        contributionRates = ", ".join([str(row.get("Contribution 1")), str(row.get("Contribution 2")), str(row.get("Contribution 3")),
                                       str(row.get("Contribution 4")), str(row.get("Contribution 5"))])
        projectedContributionRates = ", ".join([str(row.get("Projected Contribution 1")), str(row.get("Projected Contribution 2")),
                                                str(row.get("Projected Contribution 3")), str(row.get("Projected Contribution 4")),
                                                str(row.get("Projected Contribution 5"))])
        fundSize = row.get("Fund Size")
        print "type of fundSize : {}".format(type(fundSize))
        if type(fundSize) != float:
            fundSize = "null"
        else:
            fundSize *= 1000000

        statement = ("UPDATE Fund SET familyId = \'{}\', fundStyleId = \'{}\', clientId = {}, designation = \'{}\', "
                "growth = {}, yield = {}, bow = {}, investYears = {}, life = {}, vintageYear = \'{}\', "
                "closeDate = \'{}\', investStartDate = \'{}\', fundSize = {}, currency = \'{}\', commitment = {}, "
                "contributionRates = \'{}\', projectedGrowth = {}, projectedYield = {}, projectedBow = {}, projectedInvestYears = {}, "
                     "projectedLife = {}, projectedContributionRates = \'{}\' WHERE fundId = \'{}\'")

        query = statement.format(row.get("Fund Family").encode('utf-8'), fundStyleId, fundClientId, row.get("Designation"),
                                 row.get("Growth Rate"), row.get("Yield"),row.get("Bow"), row.get("Invest Years"),
                                 row.get("Life"), row.get("Vintage Year"),row.get("Close Date"),
                                 row.get("Invest Start Date"), fundSize, row.get("Currency"),
                                 row.get("Commitment") * 1000000, contributionRates, row.get("Projected Growth"),
                                 row.get("Projected Yield"), row.get("Projected Bow"), row.get("Projected Invest Years"),
                                 row.get("Projected Life"), projectedContributionRates, row.get("ID Code"))

        #print query
        self.CashFlowDB.queryDB(query)


    # Creates a new fund and adds statistics to it.
    def _addFund(self, row):
        fundId = row[1].get("ID Code")
        query = ("INSERT INTO Fund (fundId) VALUES (\'{}\')".format(fundId))
        self.CashFlowDB.queryDB(query)

    # Checks to see if the given query returns any results in cbaDB.
    def _rowDoesntExist(self, query):
        cursor = self.CashFlowDB.queryDB(query)
        rowHolder = cursor.fetchone()
        return rowHolder is None

    # Searches a table for a given field to find the correct Id value.
    def _findId(self, table, key, field, criteria):
        query = "SELECT {} FROM {} WHERE {} = \'{}\'".format(key, table, field, criteria)
        cursor = self.CashFlowDB.queryDB(query)
        return cursor.fetchone()[0]

    # Processes and inserts all info.
    def processAll(self):
        self.processSponsors()
        self.processFundStyleDf()
        self.processClientDf()
        self.processMergedDf()
        self.processFundInfo()

#a = ValidationReader("CBA Cash Flow Model - v2.17 Clearspring Analysis")
#a.processAll()