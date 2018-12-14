from APIs import ReaderAPI
from Classes import CashFlow
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
        return "~/Box Sync/Shared/Lock-up Fund Client Holdings & Performance Tracker/Cash Flow Model/{}.xlsx".format(self.fileName)

    def getLimit(self):
        raise NotImplementedError("Not necessary to implement")

    def _read(self):
        #todo
        # Reads the Raw_Data sheet, deletes rows where fund is na, and iterates over the rows
        raw_data = pd.read_excel(ospath(self.getFileName()), sheet_name="Raw_Data", header=1)

        raw_data = self._cleanData(raw_data)

        for row in raw_data.iterrows():
            self._processRow(row[1])


    # Cleans the dataframe before it is to be processed
    def _cleanData(self, raw_data):

        # Rows don't necessarily need to be removed, but are not used in creating rows.
        try:
            raw_data = raw_data.drop(columns = ['Unnamed: 14', 'Unnamed: 15', 'add XIRR using arrays, and terminal value based on max(date).', 'Unnamed: 17'])
        except KeyError:
            pass
        # Removes rows that do not have a fund code
        raw_data = raw_data[raw_data["Fund Code"].notna()]

        # Creates empty string for the type and notes if they are na

        raw_data['Notes'] = raw_data['Notes'].fillna('')
        raw_data['Type'] = raw_data['Type'].fillna('')
        # Encode into utf-8 to avoid unusual symbols
        raw_data['Notes'] = raw_data['Notes'].str.encode('utf-8')
        raw_data['Type'] = raw_data['Type'].str.encode('utf-8')
        # items in Notes not reading:
        # CCDD062016AF , CSPE032015AF , QCVD032017AF , DWPE042016M2
        # has formulas that are coming up as nan ... if encoded first they will end up being removed

        return raw_data

    def _processRow(self, row):
        # Empty Rows
        if self._isUselessRow(row):
            return
        # Need to run sponsor data table sheet before fund is added...
        elif not self._fundExists(row.get("Fund Code")):
            raise ValueError("No valid fund. Try checking the Sponsor Data Table sheet")
        elif self._isCommitment(row):
            self._makeInitialCommitment(row)
            print "MADE INITIAL COMMITMENT"
        elif self._isQtr(row):
            self._makeQtr(row)
            print "MADE QTR"
        elif self._isSimpleRow(row):
            self._makeSimpleRow(row)
            print "MADE SIMPLE ROW"
        elif self._isInferredRow(row):
            self._makeInferredRow(row)
            print "MADE INFERRED ROW"
        else:
            # ignore the base cash flow value and make multiple inputs
            self._makeComplexRow(row)
            print "MADE COMPLEX ROW"


    # From old code before the data was cleaned... may not be needed.
    # Previously checked if fundID did not exists or too many $- in certain areas.
    def _isUselessRow(self, row):
        #todo... what to include since data was cleaned a bit?
        return False

    # Determines if the fund already exists in the database.
    #todo test
    def _fundExists(self, code):
        query = "SELECT fundID FROM fund WHERE fundID = \'{}\'".format(code)
        cursor = self.CashFlowDB.queryDB(query)
        temp = cursor.fetchone()
        print temp
        return temp is not None

    # Determines if a given row is an initial commitment value.
    def _isCommitment(self, row):
        noCashFlow = (pd.isna(row['Cash Flow'])) or row['Cash Flow'] == 0
        hasCommitment = (pd.notna(row['Commitment']))
        noQtr = (pd.isna(row['Qtr Valuation']))
        return noCashFlow and hasCommitment and noQtr

    # Makes an initial commitment value, should only occur after the fundID is initially read through sponsor data table file.
    def _makeInitialCommitment(self, row):
        fundID = row['Fund Code']
        date = row['Date']
        value = row['Commitment']
        typeID = self._findNamedType('Balance', 'Initial Commitment')
        notes = row['Notes']
        result = CashFlow.CashFlow(fundID, date, value, typeID, notes)
        self._processCashFlow(result)

    # Queries the DB for a CashFlowType with given result and useCase.
    # todo possibly need to cast result to str type, was done in previous code
    def _findNamedType(self, result, useCase):
        query = "SELECT typeID FROM CashFlowType WHERE result = \'{}\' AND useCase = \'{}\'".format(result, useCase)
        cursor = self.CashFlowDB.queryDB(query)
        return cursor.fetchone()[0]

    # Tries to add a CashFlow object into the CashFlow table in the DB.
    def _processCashFlow(self, cashflow):
        check = ("SELECT * FROM CashFlow WHERE fundID=\'{}\' AND cfDate=\'{}\' AND cashValue={} AND typeID={}"
                 " AND notes=\'{}\'".format(cashflow.getFundID(), cashflow.getDate(), cashflow.getValue(),
                                            cashflow.getTypeID(), cashflow.getNotes()))
        cursor = self.CashFlowDB.queryDB(check)
        rowHolder = cursor.fetchone()
        if rowHolder is None:
            query = ("INSERT INTO CashFlow (fundID, cfDate, cashValue, typeID, notes) VALUES (\'{}\', \'{}\', {}, {}, \'{}\'".format(
                cashflow.getFundID(), cashflow.getDate(), cashflow.getValue(), cashflow.getTypeID(), cashflow.getNotes()))
            #self.CashFlowDB.queryDB(query)
            print query

    # Determines if a given row is a Quarter Valuation.
    def _isQtr(self, row):
        return pd.notna(row["Qtr Valuation"])

    # Makes a CashFlow specifically for Quarter Valuations.
    def _makeQtr(self, row):
        fundID = row['Fund Code']
        date = row['Date']
        value = row['Qtr Valuation']
        typeID = self._findNamedType('Balance', 'Quarterly Valuation')
        notes = row['Notes']
        result = CashFlow.CashFlow(fundID, date, value, typeID, notes)
        self._processCashFlow(result)

    # Determines if the given row is a simple row, ie if there is a cash flow but no other values(Expenses, ROC, Dist. Sub. To Recall, Income).
    def _isSimpleRow(self, row):
        return (pd.notna(row['Cash Flow']) and pd.isna(row['Expenses']) and pd.isna(row['ROC']) and
                pd.isna(row['Dist. Sub. To Recall']) and pd.isna(row['Income']))

    # Creates a CashFlow for a simple row.
    def _makeSimpleRow(self, row):
        fundID = row['Fund Code']
        date = row['Date']
        value = row['Cash Flow']
        typeID = self._findSimpleTypeID(row)
        notes = row['Notes']
        result = CashFlow.CashFlow(fundID, date, value, typeID, notes)
        self._processCashFlow(result)

    # Looks up the CashFlowType for simple rows.
    def _findSimpleTypeID(self, row):
        result = ""
        useCase = ""
        excelType = row['Type'].lower()
        cash = row['Cash Flow']
        if 'fee' in excelType:
            result = 'Contribution'
            useCase = 'Expenses'
        elif 'contribution' in excelType or 'investment' in excelType:
            result = 'Contribution'
            useCase = 'Investment'
        elif 'income' in excelType:
            result = 'Distribution'
            useCase = 'Income'
        elif 'return of capital' in excelType:
            result = 'Distribution'
            useCase = 'Return of Capital'
        elif 'distribution' in excelType or cash > 0:
            result = 'Distribution'
            useCase = 'Standard'
        elif cash < 0:
            result = 'Contribution'
            useCase = 'Investment'
        else:
            return None

        return self._findNamedType(result, useCase)

    # Determines if a given row has inferred values, ie if there is an implied difference somewhere.
    def _isInferredRow(self, row):
        cashFlow = row['Cash Flow']
        expenses = row['Expenses']
        roc = row['ROC']
        income = row['Income']

        # Separated for readability
        if pd.notna(expenses) and expenses != cashFlow:
            return True
        elif pd.notna(roc) and ((pd.notna(income) and roc + income != cashFlow) or (roc != cashFlow and pd.isna(income))):
            return True
        else:
            return False

    # Makes the explicit and inferred rows
    def _makeInferredRow(self, row):
        cashFlow = row['Cash Flow']
        expenses = row['Expenses']
        roc = row['ROC']
        income = row['Income']

        net = cashFlow
        otherValue = None
        typeID = None

        if pd.isna(expenses):
            net -= roc
            otherValue = roc
            temp = self._findResult(row, 'ROC')
            typeID = self._findNamedType(temp, "Return of Capital")
        elif pd.isna(roc):
            net -= expenses
            otherValue = expenses
            temp = self._findResult(row, 'Expenses')
            typeID = self._findNamedType(temp, "Expenses")
        else:
            raise ValueError("Invalid data for inferred row")

        fundID = row['Fund Code']
        date = row['Date']
        notes = row['Notes']
        netRow = CashFlow.CashFlow(fundID, date, net, typeID, notes)
        otherRow = CashFlow.CashFlow(fundID, date, otherValue, typeID, notes)
        self._processCashFlow(netRow)
        self._processCashFlow(otherRow)

    # Determines whether the element in row[column] should be a contribution or distribution
    def _findResult(self, row, column):
        excelType = row['Type'].lower()
        notes = str(row['Notes']).lower()
        if 'contribution' in excelType or 'contribution' in notes:
            return 'Contribution'
        elif 'distribution' in excelType or 'distribution' in notes:
            return 'Distribution'
        # Split up b/c checking in the notes/excel type is a priority
        elif column == 'Expenses':
            return 'Contribution'
        elif column == 'ROC' or column == 'Dist. Sub. To Recall' or column == 'Income':
            return 'Distribution'
        else:
            raise ValueError

    # Makes complex rows depending on the excel cash flow.
    def _makeComplexRow(self, row):
        useCases = {'Expenses':'Expenses', 'ROC':'Return of Capital', 'Dist. Sub. To Recall':'Subject to Recall', 'Income':'Income'}
        for case in useCases:
            if pd.notna(row[case]):
                fundID = row['Fund Code']
                date = row['Date']
                value = row[case]
                temp = self._findResult(row, case)
                typeID = self._findNamedType(temp, useCases[case])
                notes = row['Notes']
                result = CashFlow.CashFlow(fundID, date, value, typeID, notes)
                self._processCashFlow(result)

#a = Reader("CBA Cash Flow Model - v2.17 Clearspring Analysis")
