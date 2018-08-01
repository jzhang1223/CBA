from APIs import QueryAPI
#from Classes import Reader
import pymysql.cursors
import datetime

# Make this the class that has the connection?
class Query(QueryAPI.QueryAPI):

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cba71118',
                                 db='cbaDB')


    def getFundTransactions(self, fundID):
        try:
            #with self.connection.cursor() as cursor:
            query = "SELECT * FROM CashFlow WHERE fundID = '" + fundID + "'"
            #    cursor.execute(query)
            #    self._printResult(cursor)
            self.queryDB(query)
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
            with self.connection.cursor() as cursor:
                print query
                cursor.execute(query)
                self.connection.commit()
                return cursor
        except Exception as e:
            print e

fundID = 'CCDD062016AF'
endDate = datetime.datetime.strptime('4/2/18', '%m/%d/%y')
a = Query()
print a.queryDB(
            "SELECT cfDate, cashValue FROM CashFlow "
            "WHERE fundID = '{}' AND cfDate <= '{}'".format(fundID, endDate)).fetchall()

