class ValidationTable(object):

    def sameItem(self, other):
        raise NotImplementedError("Interface method called")

class Sponsor(ValidationTable):

    def __init__(self, sponsorId, sponsorName):
        self.sponsorId = sponsorId
        self.sponsorName = sponsorName

    def getSponsorId(self):
        return self.sponsorId

    def getSponsorName(self):
        return self.sponsorName

    def sameItem(self, other):
        return type(other) == type(self) and \
               self.getSponsorId() == other.getSponsorId() and \
               self.getSponsorName() == other.getSponsorName()

class FundClient(ValidationTable):

    def __init__(self, clientId, clientName):
        self.clientId = clientId
        self.clientName = clientName

    def getClientId(self):
        return self.clientId

    def getClientName(self):
        return self.clientName

    def sameItem(self, other):
        return type(other) == type(self) and \
            self.getClientId() == other.getClientId() and \
            self.getClientName() == other.getClientName()

class FundStyle(ValidationTable):

    def __init__(self, fundStyleId, fundStyleName):
        self.fundStyleId = fundStyleId
        self.fundStyleName = fundStyleName

    def getFundStyleId(self):
        return self.fundStyleId

    def getfundStyleName(self):
        return self.fundStyleName

    def sameItem(self, other):
        return type(other) == type(self) and \
            self.getFundStyleId() == other.getFundStyleId() and \
            self.getfundStyleName() == other.getfundStyleName()

class Family(ValidationTable):

    def __init__(self, familyName, sponsorId):
        self.familyName = familyName
        self.sponsorId = sponsorId

    def getFamilyName(self):
        return self.familyName

    def getSponsorId(self):
        return self.sponsorId

    def sameItem(self, other):
        return type(other) == type(self) and \
            self.getFamilyName() == other.getFamilyName() and \
            self.getSponsorId() == other.getSponsorId()


