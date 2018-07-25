from APIs import QueryAPI
#from Classes import Reader
import pymysql.cursors

# Make this the class that has the connection?
class Query(QueryAPI.QueryAPI):

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cba71118',
                                 db='cbaDB')


    def getFundTransactions(self, fundID):
        try:
            with connection.cursor() as cursor:
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


    def queryDB(self, query):
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor
        except Exception as e:
            print e