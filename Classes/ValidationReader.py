import pandas as pd
from os.path import expanduser as ospath
import Query
import ValidationTables

class ValidationReader(object):

    def __init__(self, fileVersion="2.14"):
        self.CashFlowDB = Query.Query()
        self.fileVersion = fileVersion
        self.filePath = '~/Box Sync/Shared/Lock-up Fund Client Holdings & Performance Tracker/Cash Flow Model/CBA Cash Flow Model - v{} - Far Hills.xlsx'.format(fileVersion)
        self.validationDf = pd.read_excel(ospath(self.filePath), sheet_name='Validation', header=1)
        self.sponsorDataTableDf = pd.read_excel(ospath(self.filePath), sheet_name='Sponsor Data Table', header=1)[
            ["ID Code", "Client", "Sponsor", "Fund Family", "Designation", "Fund Style", "Vintage Year", "Close Date",
             "Invest Start Date", "Contribution (% of Rem. Commit)", "Unnamed: 14", "Unnamed: 15", "Unnamed: 16", "Unnamed: 17",
             "Model Metrics", "Unnamed: 19", "Unnamed: 20", "Model Years to", "Unnamed: 23"]]
        # Renamming the columns to be readable
        self.sponsorDataTableDf.columns = ["ID Code", "Client", "Sponsor", "Fund Family", "Designation", "Fund Style", "Vintage Year", "Close Date",
             "Invest Start Date", "Contribution 1", "Contribution 2", "Contribution 3", "Contribution 4", "Contribution 5",
             "Bow", "Growth", "Yield", "Invest Years", "Life"]
        self.sponsorDataTableDf = self.sponsorDataTableDf[self.sponsorDataTableDf["ID Code"].notna()]

        # Should probably be abstracted given more time
        self.initializeClientDf()
        self.initializeFundStyleDf()
        self.initializeSponsors()
        self.initializeMergedDf()

        #self.processSponsors()

    def initializeSponsors(self):
        self.sponsorDf = self.validationDf[['Sponsor_List', 'Sponsor_Code']]
        self.sponsorDf = self.sponsorDf.dropna()
        self.sponsorDf['Sponsor_List'] = self.sponsorDf['Sponsor_List'].str.strip()

    def initializeFundStyleDf(self):
        self.fundStyleDf = self.validationDf[['Fund_Style', 'Fund_Code']]
        self.fundStyleDf = self.fundStyleDf.dropna()
        self.fundStyleDf['Fund_Style'] = self.fundStyleDf['Fund_Style'].str.strip()

    def initializeClientDf(self):
        self.clientDf = self.validationDf[["Client_List", "Client_Code"]]
        self.clientDf = self.clientDf.dropna()
        self.clientDf['Client_List'] = self.clientDf['Client_List'].str.strip()

    def initializeMergedDf(self):
        self.familyDf = self.sponsorDataTableDf[["Sponsor", "Fund Family"]]
        self.familyDf = self.familyDf.dropna()
        self.familyDf['Sponsor'] = self.familyDf['Sponsor'].str.strip()
        self.familyDf['Fund Family'] = self.familyDf['Fund Family'].str.strip()

        self.mergedDf = pd.merge(self.sponsorDf, self.familyDf, left_on='Sponsor_List', right_on='Sponsor')[
            ['Sponsor_Code', 'Fund Family']]
        self.mergedDf = self.mergedDf.drop_duplicates()

    def processSponsors(self):
        for row in self.sponsorDf.iterrows():
            rowItem = ValidationTables.Sponsor(row[1].get("Sponsor_Code"), row[1].get("Sponsor_List"))
            check = ("SELECT * FROM Sponsor WHERE sponsorId=\'{}\' AND sponsorName=\'{}\'".format(
                rowItem.getSponsorId().encode('utf-8'), rowItem.getSponsorName().encode('utf-8')))
            if self._rowDoesntExist(check):
                query = ("INSERT INTO Sponsor (sponsorId, sponsorName) VALUES (\'{}\', \'{}\')".format(
                    rowItem.getSponsorId().encode('utf-8'), rowItem.getSponsorName().encode('utf-8')))
                self.CashFlowDB.queryDB(query)

    def processFundStyleDf(self):
        for row in self.fundStyleDf.iterrows():
            rowItem = ValidationTables.FundStyle(row[1].get("Fund_Code"), row[1].get("Fund_Style"))
            check = ("SELECT * FROM FundStyle WHERE fundStyleId=\'{}\' AND fundStyleName=\'{}\'".format(
                rowItem.getFundStyleId().encode('utf-8'), rowItem.getfundStyleName().encode('utf-8')))
            if self._rowDoesntExist(check):
                query = ("INSERT INTO FundStyle (fundStyleId, fundStyleName) VALUES (\'{}\', \'{}\')".format(
                    rowItem.getFundStyleId().encode('utf-8'), rowItem.getfundStyleName().encode('utf-8')))
                self.CashFlowDB.queryDB(query)


    def processClientDf(self):
        for row in self.clientDf.iterrows():
            rowItem = ValidationTables.FundClient(row[1].get("Client_Code"), row[1].get("Client_List"))
            check = ("SELECT * FROM FundClient WHERE clientId=\'{}\' AND clientName=\'{}\'".format(
                rowItem.getClientId().encode('utf-8'), rowItem.getClientName().encode('utf-8')))
            if self._rowDoesntExist(check):
                query = ("INSERT INTO FundClient (clientId, clientName) VALUES (\'{}\', \'{}\')".format(
                    rowItem.getClientId().encode('utf-8'), rowItem.getClientName().encode('utf-8')))
                self.CashFlowDB.queryDB(query)

    #Inserts data into the Family table
    def processMergedDf(self):
        for row in self.mergedDf.iterrows():
            rowItem = ValidationTables.Family(row[1].get("Fund Family"), row[1].get("Sponsor_Code"))
            check = ("SELECT * FROM Family WHERE familyName=\'{}\' AND sponsorId=\'{}\'".format(
                rowItem.getFamilyName().encode('utf-8'), rowItem.getSponsorId().encode('utf-8')))
            if self._rowDoesntExist(check):
                query = ("INSERT INTO Family (familyName, sponsorId) VALUES (\'{}\', \'{}\')".format(
                    rowItem.getFamilyName().encode('utf-8'), rowItem.getSponsorId().encode('utf-8')))
                self.CashFlowDB.queryDB(query)

    def processFundInfo(self):
        fundDataDf = self.sponsorDataTableDf[self.sponsorDataTableDf["ID Code"].notna()]
        for row in fundDataDf.iterrows():
            check = ("SELECT * FROM Fund WHERE fundId=\'{}\'".format(row[1].get("ID Code")))
            if self._rowDoesntExist(check):
                self._addFund(row)
                self._appendFund(row)
                print "Adding new row"
            else:
                self._appendFund(row)
                print "Appending to existing row"


    # Adds all statistics to an existing fund that needs more info
    def _appendFund(self, row):
        # FamilyID PK is just the family name so its OK
        fundStyleId = self._findId("FundStyle", "fundStyleId", "fundStyleName", row[1].get("Fund Style"))
        if pd.isnull(row[1].get("Client")):
            fundClientId = "null"
        else:
            fundClientId = "\'{}\'".format(self._findId("FundClient", "clientId", "clientName", row[1].get("Client")))

        contributionRates = ", ".join([str(row[1].get("Contribution 1")), str(row[1].get("Contribution 2")), str(row[1].get("Contribution 3")),
                                       str(row[1].get("Contribution 4")), str(row[1].get("Contribution 5"))])

        statement = ("UPDATE Fund SET familyId = \'{}\', fundStyleId = \'{}\', clientId = {}, designation = \'{}\', "
                 "growth = {}, yield = {}, bow = {}, investYears = {}, life = {}, vintageYear = \'{}\', "
                 "closeDate = \'{}\', investStartDate = \'{}\', contributionRates = \'{}\' WHERE fundId = \'{}\'")
        query = statement.format(row[1].get("Fund Family").encode('utf-8'), fundStyleId, fundClientId, row[1].get("Designation"),
                                 row[1].get("Growth"), row[1].get("Yield"),row[1].get("Bow"),
                                 row[1].get("Invest Years"),row[1].get("Life"), row[1].get("Vintage Year"),
                                 row[1].get("Close Date"), row[1].get("Invest Start Date"), contributionRates,
                                 row[1].get("ID Code"))

        print query


    # Creates a new fund and adds statistics to it
    def _addFund(self, row):
        fundId = row[1].get("ID Code")
        query = ("INSERT INTO Fund (fundId) VALUES (\'{}\')".format(fundId))
        print query

    # Checks to see if the given query returns any results in cbaDB
    def _rowDoesntExist(self, query):
        cursor = self.CashFlowDB.queryDB(query)
        rowHolder = cursor.fetchone()
        return rowHolder is None

    # Searches a table for a given field to find the correct Id value
    def _findId(self, table, key, field, criteria):
        query = "SELECT {} FROM {} WHERE {} = \'{}\'".format(key, table, field, criteria)
        cursor = self.CashFlowDB.queryDB(query)
        return cursor.fetchone()[0]

a = ValidationReader()
print a.sponsorDataTableDf["Client"]
a.processFundInfo()
