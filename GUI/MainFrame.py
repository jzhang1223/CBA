import Tkinter as tk
import FundModel as fm
import inspect
import pandas as pd
pd.set_option("display.max_rows", 10000)

class Application(tk.Frame):


    def createWidgets(self):
        # Title of window
        self.fundModel = None
        self.winfo_toplevel().title("INSERT TITLE HERE")

        # Quit buttons
        self.QUIT = tk.Button(self, text = "QUIT", command = self.quit)
        self.QUIT.grid(row = 0, column = 0)

        self.RESET = tk.Button(self, text = "Reset Model", command = self._resetAll)
        self.RESET.grid(row = 0, column = 1)

        self.CLEARINPUTS = tk.Button(self, text = "Clear Inputs", command = self._clearInputs)
        self.CLEARINPUTS.grid(row = 0, column = 2)

        self.FILLINPUTS = tk.Button(self, text = "Fill Inputs", command = self._fillInputs)
        self.FILLINPUTS.grid(row = 0, column = 3)

        self.SUBMIT = tk.Button(self, text = "Create Model", command = self._createModel)
        self.SUBMIT.grid(row = 0, column = 4)

        self.EXPORT = tk.Button(self, text = "Export Model", command = self._exportPopup)
        self.EXPORT.grid(row = 0, column = 5)

        self.STATUS = tk.Label(self)
        self.STATUS.grid(row = 0, column = 6)

        self.MODELTYPE = tk.IntVar()
        self.PROJECTIONBUTTON = tk.Radiobutton(self, text="Projection Only", variable=self.MODELTYPE, value=0)
        self.ACTUALBUTTON = tk.Radiobutton(self, text="Actuals Only", variable=self.MODELTYPE, value=1)
        self.ACTUALANDPROJECTIONBUTTON = tk.Radiobutton(self, text="Actuals + Projection", variable=self.MODELTYPE, value=2)
        self.PROJECTIONBUTTON.grid(row = 0, column = 7)
        self.ACTUALBUTTON.grid(row = 0, column = 8)
        self.ACTUALANDPROJECTIONBUTTON.grid(row = 0, column = 9)

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
        self._resetAll()
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

    # Forecasts the model based on the selected radiobutton.
    def _forecastModel(self):
        print "FORECASTING MODEL"
        if self.MODELTYPE.get() > 0:
            self.fundModel.setActualValues(self.fundNameTEXT.get())
        if self.MODELTYPE.get() != 1:
            self.fundModel.forecastValues()
            #print self.fundModel._formatModelToDataframe()
        self._createOutput(self.fundModel._formatModelToDataframe())

    # Fill in the inputs based on the fundId given
    def _fillInputs(self):
        #commitment, segments
        if (self.fundNameTEXT.get() == ""):
            self.setStatus("No fund name given")
            return
        import Query
        CashflowDB = Query.Query()
        query = ("SELECT contributionRates, bow, growth, yield, investYears, life, investStartDate "
                 "FROM Fund WHERE fundID = \'{}\'".format(self.fundNameTEXT.get()))
        result = CashflowDB.queryDB(query).fetchone()
        commitmentQuery = "SELECT capitalCommited(\'{}\')".format(self.fundNameTEXT.get())
        commitmentResult = CashflowDB.queryDB(commitmentQuery).fetchone()[0]
        print commitmentResult
        self.capitalCommitmentTEXT.insert(0, str(commitmentResult))
        self.contributionRatesTEXT.insert(0, result[0])
        self.bowTEXT.insert(0, result[1])
        self.growthRateTEXT.insert(0, result[2])
        self.fundYieldTEXT.insert(0, result[3])
        self.lastInvestmentYearTEXT.insert(0, result[4])
        self.lifeOfFundTEXT.insert(0, result[5])
        startDate = result[6].date()
        self.startDateTEXT.insert(0, "{}-{}-{}".format(str(startDate.year)[2:], startDate.month, startDate.day))

        # Get inputs if exists
        # Fill into correct spots
        # Give status

    def _createOutput(self, output):
        if hasattr(self, 'OUTPUT'):
            self.OUTPUT.grid_forget()
        print "PRINTING OUTPUT"
        print output.to_string()
        self.OUTPUT = tk.Label(self, text = "\n".join(output.index.tolist()))

        self.OUTPUT.grid(row = 2, column = 0)
        self.outputList.append(self.OUTPUT)

        for i in range(0, len(output.columns)):
            self.OUTPUT = tk.Label(self, text = str(output[i].to_string(index = False)), width = 10)
            #self.OUTPUT = tk.Message(text = output.to_string())
            self.OUTPUT.grid(row = 2, column = i + 1)
            self.outputList.append(self.OUTPUT)

        self.setStatus("FORCASTED")

    # Resets the model and all text boxes.
    def _resetAll(self):
        print "RESETING MODEL"
        self.fundModel = None
        self._clearOutputs()
        self.setStatus("MODEL RESET")


    # Save the data to an file.
    #todo
    def _saveData(self):
        print "saving data..."

    # Clears the inputs to the entry boxes.
    def _clearInputs(self):
        for textBox in self.textBoxList:
            textBox.delete(0, tk.END)
        self.setStatus("Inputs Cleared")

    # Removes the output from the screen.
    def _clearOutputs(self):
        for output in self.outputList:
            output.grid_forget()
        self.setStatus("Outputs Cleared")

    # Opens a popup for exporting the model
    def _exportPopup(self):
        if self.fundModel is None:
            self.setStatus("Model has not yet been created")
        else:
            #todo
            top = tk.Toplevel()
            top.title("Export Menu")
            text = tk.Message(top, text = "Export File As (.csv extension is already included):")
            text.pack()
            fileEntry = tk.Entry(top)
            fileEntry.pack()
            confirmButton = tk.Button(top, text = "Confirm Export", command = lambda: self._exportModel(top, fileEntry.get()))
            confirmButton.pack()
            cancelButton = tk.Button(top, text = "Cancel", command = top.destroy)
            cancelButton.pack()

    # Exports the model to a csv file
    def _exportModel(self, widget, fileName):
        self.fundModel.exportToCsv("{}.csv".format(fileName))
        widget.destroy()
        self.setStatus("Saved {}.csv".format(fileName))

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