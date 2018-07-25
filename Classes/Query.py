from APIs import QueryAPI
from Classes import Reader

class Query(QueryAPI.QueryAPI):

    
    def getFundTransactions(self, fundID):
        try:
            with Reader.connection.cursor() as cursor:
                query = "SELECT * FROM CashFlow WHERE fundID = '" + fundID + "'"
                cursor.execute(query)
                self._printResult(cursor)
        except Exception as e:
            print e


    def remainingCommitment(self, fundID, endDate):
        return NotImplementedError("Todo")
    def currentNAV(self, fundID, endDate):
        return NotImplementedError("Todo")
    def getGrowth(self, fundID):
        return NotImplementedError("Todo")

    def _printResult(self, cursor):
        for i in cursor:
            print i