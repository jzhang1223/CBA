import Tkinter as tk
import FundModel as fm
import inspect

class Application(tk.Frame):

    def createWidgets(self):
        self.QUIT = tk.Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self._setupFundModel()

        self.SUBMIT = tk.Button(self)
        self.SUBMIT["text"] = "Create Model"
        self.SUBMIT["command"] = self._createModel
        self.SUBMIT.pack({"side": "left"})
    '''
        self.FUNDNAME = tk.Entry(self)

        self.FUNDNAME.pack({"side": "left"})
    '''


    # Sets up the components for entering Fund Model Data
    def _setupFundModel(self):
        for argument in inspect.getargspec(fm.FundModel.__init__)[0]:

            if argument != 'self':
                # make labels for the textbox
                setattr(self, argument + "LABEL", tk.Label(self, text = argument))
                # make the text box
                setattr(self, argument + "TEXT", tk.Entry(self, width=10))
                # pack the label, box
                getattr(self, argument + "LABEL").pack({"side": "left"})
                getattr(self, argument + "TEXT").pack({"side": "left"})
                print argument


    def _createModel(self):
        capitalCommitment = self.capitalCommitmentTEXT.get()
        contributionRates = self.contributionRatesTEXT.get()
        bow = self.bowTEXT.get()
        growthRate = self.growthRateTEXT.get()
        fundYield = self.fundYieldTEXT.get()
        lastInvestmentYear = self.lastInvestmentYearTEXT.get()
        lifeOfFund = self.lifeOfFundTEXT.get()
        segments = self.segmentsTEXT.get()
        startDate = self.startDateTEXT.get()
        print capitalCommitment
        print contributionRates
        print bow
        print growthRate
        print fundYield
        print lastInvestmentYear
        print lifeOfFund
        print segments
        print startDate
        self.fundModel = fm.FundModel(capitalCommitment, contributionRates, bow, growthRate, fundYield,
                                    lastInvestmentYear, lifeOfFund, segments, startDate)
            #raise ValueError("Check your data again")

    # Aquires the actual data to add to the FundModel.
    def _makeActuals(self):
        pass #todo

    # Save the data to an file.
    def _saveData(self):
        print "saving data..."

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
root.destroy()