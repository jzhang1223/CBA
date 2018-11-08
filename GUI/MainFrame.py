import Tkinter as tk
import FundModel as fm
import inspect
import pandas as pd
pd.set_option("display.max_rows", 10000)

class Application(tk.Frame):


    def createWidgets(self):
        # Title of window
        self.winfo_toplevel().title("INSERT TITLE HERE")

        # Quit buttons
        self.QUIT = tk.Button(self)
        self.QUIT["text"] = "QUIT"
        #self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.grid(row = 0, column = 0)

        self.RESET = tk.Button(self)
        self.RESET["text"] = "Reset Model"
        self.RESET["command"] = self._resetAll
        self.RESET.grid(row = 0, column = 1)

        self.CLEARINPUTS = tk.Button(self)
        self.CLEARINPUTS["text"] = "Clear Inputs"
        self.CLEARINPUTS["command"] = self._clearInputs
        self.CLEARINPUTS.grid(row = 0, column = 2)

        self.CLEAROUTPUTS = tk.Button(self)
        self.CLEAROUTPUTS["text"] = "Clear Outputs"
        self.CLEAROUTPUTS["command"] = self._clearOutputs
        self.CLEAROUTPUTS.grid(row = 0, column = 3)

        self.SUBMIT = tk.Button(self)
        self.SUBMIT["text"] = "Create Model"
        self.SUBMIT["command"] = self._createModel
        self.SUBMIT.grid(row = 0, column = 4)

        self.STATUS = tk.Label(self)
        self.STATUS.grid(row = 0, column = 5)

        self._setupEntryWidgets()

    '''
        self.FORECAST = tk.Button(self)
        self.FORECAST["text"] = "Forecast Model"
        self.FORECAST["command"] = self._forecastModel
        self.FORECAST.grid(row = 0, column = 3)

    
        self.FUNDNAME = tk.Entry(self)

        self.FUNDNAME.pack({"side": "left"})
    '''


    # Sets up the components for entering Fund Model Data
    def _setupEntryWidgets(self):
        self.textBoxList = []
        self.outputList = []
        count = 0
        print "SETTING UP ENTRY WIDGETS"
        for argument in inspect.getargspec(fm.FundModel.__init__)[0]:
            if argument != 'self':

                # make labels for the textbox
                setattr(self, argument + "LABEL", tk.Label(self, text = argument))
                # make the text box
                setattr(self, argument + "TEXT", tk.Entry(self, width = 7))
                # pack the label, box
                getattr(self, argument + "LABEL").grid(row = 1, column = count)
                getattr(self, argument + "TEXT").grid(row = 1, column = count + 1)

                # Add to master list of widgets for easy clearing.
                self.textBoxList.append(getattr(self, argument + "TEXT"))
                count += 2
                print argument
        self.fundNameLABEL = tk.Label(self, text = "fundName")
        self.fundNameTEXT = tk.Entry(self, width = 7)
        self.fundNameLABEL.grid(row = 1, column = count)
        self.fundNameTEXT.grid(row= 1, column= count + 1)


    def _createModel(self):
        print "CREATING MODEL"
        capitalCommitment = self.capitalCommitmentTEXT.get()
        # Needs to accept contributionRates delimited by ", ".
        contributionRates = [float(x) for x in self.contributionRatesTEXT.get().split(", ")]
        bow = self.bowTEXT.get()
        growthRate = self.growthRateTEXT.get()
        fundYield = self.fundYieldTEXT.get()
        lastInvestmentYear = self.lastInvestmentYearTEXT.get()
        lifeOfFund = self.lifeOfFundTEXT.get()
        segments = self.segmentsTEXT.get()
        startDate = self.startDateTEXT.get()

        self.fundModel = fm.FundModel(capitalCommitment, contributionRates, bow, growthRate, fundYield,
                                    lastInvestmentYear, lifeOfFund, segments, startDate)
        print self.fundModel.capitalCommitment
        print self.fundModel.contributionRates
        print self.fundModel.bow
        print self.fundModel.growthRate
        print self.fundModel.fundYield
        print self.fundModel.lastInvestmentYear
        print self.fundModel.lifeOfFund
        print self.fundModel.segments
        print self.fundModel.startDate
            #raise ValueError("Check your data again")
        self._forecastModel()

    def _forecastModel(self):
        print "FORECASTING MODEL"
        self.fundModel.forecastValues()
        print self.fundModel._formatModelToDataframe()
        self._createOutput(self.fundModel._formatModelToDataframe())

    # Aquires the actual data to add to the FundModel.
    def _makeActuals(self):
        pass #todo

    def _createOutput(self, output):
        #for i in range(len(self.fundModel))
        if hasattr(self, 'OUTPUT'):
            self.OUTPUT.grid_forget()
        print output.to_string()
        self.OUTPUT = tk.Label(self, text = "\n".join(output.index.tolist()))


        print output.index.tolist()
        print "\n".join(output.index.tolist())
        #self.OUTPUT = tk.Label(self, text = "'ua\nb\nc\nd\ne\nf\ng")
        self.OUTPUT.grid(row = 2, column = 0)
        self.outputList.append(self.OUTPUT)

        for i in range(0, len(output.columns)):
            self.OUTPUT = tk.Label(self, text = str(output[i].to_string(index = False)), width = 10)
            #self.OUTPUT = tk.Message(text = output.to_string())
            self.OUTPUT.grid(row = 2, column = i + 1)
            self.outputList.append(self.OUTPUT)

        print type(output[1].to_string(index = False))
        print output[1].to_string(index=False)

        self.setStatus("FORCASTED")

    # Resets the model and all text boxes.
    # Possibly clear or not clear the text boxes. If not cleared, needs something to tell the user data is reset. todo
    def _resetAll(self):
        print "RESETING MODEL"
        self.fundModel = None
        self.setStatus("MODEL RESET")

    # Save the data to an file.
    def _saveData(self):
        print "saving data..."

    # Clears the inputs to the entry boxes
    def _clearInputs(self):
        for textBox in self.textBoxList:
            textBox.delete(0, tk.END)
        self.setStatus("Inputs Cleared")

    def _clearOutputs(self):
        for output in self.outputList:
            output.grid_forget()
        self.setStatus("Outputs Cleared")

    # Sets the status of the GUI to the STATUS label
    def setStatus(self, status):
        self.STATUS["text"] = status

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
root.destroy()