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
        self.sponsorDataTableDf = pd.read_excel(ospath(self.filePath), sheet_name='Sponsor Data Table', header=1)

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
            cursor = self.CashFlowDB.queryDB(check)
            rowHolder = cursor.fetchone()
            if rowHolder is None:
                query = ("INSERT INTO Sponsor (sponsorId, sponsorName) VALUES (\'{}\', \'{}\')".format(
                    rowItem.getSponsorId().encode('utf-8'), rowItem.getSponsorName().encode('utf-8')))
                self.CashFlowDB.queryDB(query)

    def processFundStyleDf(self):
        for row in self.fundStyleDf.iterrows():
            rowItem = ValidationTables.FundStyle(row[1].get("Fund_Code"), row[1].get("Fund_Style"))
            check = ("SELECT * FROM FundStyle WHERE fundStyleId=\'{}\' AND fundStyleName=\'{}\'".format(
                rowItem.getFundStyleId().encode('utf-8'), rowItem.getfundStyleName().encode('utf-8')))
            cursor = self.CashFlowDB.queryDB(check)
            rowHolder = cursor.fetchone()
            if rowHolder is None:
                query = ("INSERT INTO FundStyle (fundStyleId, fundStyleName) VALUES (\'{}\', \'{}\')".format(
                    rowItem.getFundStyleId().encode('utf-8'), rowItem.getfundStyleName().encode('utf-8')))
                self.CashFlowDB.queryDB(query)


    def processClientDf(self):
        for row in self.clientDf.iterrows():
            rowItem = ValidationTables.FundClient(row[1].get("Client_Code"), row[1].get("Client_List"))
            check = ("SELECT * FROM FundClient WHERE clientId=\'{}\' AND clientName=\'{}\'".format(
                rowItem.getClientId().encode('utf-8'), rowItem.getClientName().encode('utf-8')))
            cursor = self.CashFlowDB.queryDB(check)
            rowHolder = cursor.fetchone()
            if rowHolder is None:
                query = ("INSERT INTO FundClient (clientId, clientName) VALUES (\'{}\', \'{}\')".format(
                    rowItem.getClientId().encode('utf-8'), rowItem.getClientName().encode('utf-8')))
                self.CashFlowDB.queryDB(query)

    #Inserts data into the Family table
    def processMergedDf(self):
        for row in self.mergedDf.iterrows():
            rowItem = ValidationTables.Family(row[1].get("Fund Family"), row[1].get("Sponsor_Code"))
            check = ("SELECT * FROM Family WHERE familyName=\'{}\' AND sponsorId=\'{}\'".format(
                rowItem.getFamilyName().encode('utf-8'), rowItem.getSponsorId().encode('utf-8')))
            cursor = self.CashFlowDB.queryDB(check)
            rowHolder = cursor.fetchone()
            if rowHolder is None:
                query = ("INSERT INTO Family (familyName, sponsorId) VALUES (\'{}\', \'{}\')".format(
                    rowItem.getFamilyName().encode('utf-8'), rowItem.getSponsorId().encode('utf-8')))
                self.CashFlowDB.queryDB(query)

    #### Tries to add a CashFlow object into the CashFlow table in the DB.
    def _processCashFlow(self, cashflow):
        check = ("SELECT * FROM CashFlow WHERE fundID=\'" + cashflow.getFundID() + "\' AND cfDate=\'" +
                         cashflow.getDate() + "\' AND cashValue=" + cashflow.getValue() + " AND typeID=" +
                         cashflow.getTypeID() + " AND notes=\'" + cashflow.getNotes() + "\'")
        cursor = self.CashFlowDB.queryDB(check)
        rowHolder = cursor.fetchone()
        if rowHolder is None:
            query = ("INSERT INTO CashFlow (fundID, cfDate, cashValue, typeID, notes) " + "VALUES (\'" +
                     cashflow.getFundID() + "\', \'" + cashflow.getDate() + "\', " + cashflow.getValue() + ", " +
                     cashflow.getTypeID() + ", \'" + cashflow.getNotes() + "\')")
            self.CashFlowDB.queryDB(query)

a = ValidationReader()
a.processMergedDf()