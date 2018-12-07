import Tkinter as tk
import FundModel as fm
import inspect
import pandas as pd
from Classes import Output
from Classes import ValidationReader
import datetime
from os.path import expanduser as ospath
import os.path
import ModelPeriod
pd.set_option("display.max_rows", 10000)

class Application(tk.Frame):


    def createWidgets(self):
        self.fundModel = None
        # Title of window
        self.winfo_toplevel().title("Cash Flow Model")

        # Quit buttons
        self.QUIT = tk.Button(self, text = "QUIT", command = self.quit)
        self.QUIT.grid(row = 0, column = 0)

        # Resets the model and clears the GUI output.
        self.RESET = tk.Button(self, text = "Reset Model", command = self._resetAll)
        self.RESET.grid(row = 0, column = 1)

        # Clears only the input values, excluding the fundID.
        self.CLEARINPUTS = tk.Button(self, text = "Clear Inputs", command = self._clearInputs)
        self.CLEARINPUTS.grid(row = 0, column = 2)

        # Fills in parameters based on the given fundID.
        self.FILLINPUTS = tk.Button(self, text = "Fill Inputs", command = self._fillInputs)
        self.FILLINPUTS.grid(row = 0, column = 3)

        # Button to create model base on filled in parameters, will overwrite any existing model.
        self.SUBMIT = tk.Button(self, text = "Create Model", command = self._createModel)
        self.SUBMIT.grid(row = 0, column = 4)

        # Button to export current model.
        self.EXPORT = tk.Button(self, text = "Export Model", command = self._exportPopup)
        self.EXPORT.grid(row = 0, column = 5)

        # Label for most recent status.
        self.STATUS = tk.Label(self)
        self.STATUS.grid(row = 0, column = 6)

        # Radio buttons for choosing the type of model.
        self.MODELTYPE = tk.IntVar()
        self.PROJECTIONBUTTON = tk.Radiobutton(self, text="Projection Only", variable=self.MODELTYPE, value=0)
        self.ACTUALBUTTON = tk.Radiobutton(self, text="Actuals Only", variable=self.MODELTYPE, value=1)
        self.ACTUALANDPROJECTIONBUTTON = tk.Radiobutton(self, text="Actuals + Projection", variable=self.MODELTYPE, value=2)
        self.PROJECTIONBUTTON.grid(row = 0, column = 7)
        self.ACTUALBUTTON.grid(row = 0, column = 8)
        self.ACTUALANDPROJECTIONBUTTON.grid(row = 0, column = 9)

        # Button for exporting fund stats, exports as fundStats.csv
        self.FUNDSTATS = tk.Button(self, text = "Fund Stats", command = self._exportFundStats)
        self.FUNDSTATS.grid(row = 0, column = 11)

        # Button for exporting the Base Model, Actuals, and Actuals + Projections from reading an excel sheet.
        self.MASSEXPORT = tk.Button(self, text = "Mass Export", command = self._massExportPopup)
        self.MASSEXPORT.grid(row = 0, column = 12)

        # Button to import new data that is added to the excel sheets.
        self.IMPORTDATA = tk.Button(self, text = "Import Data", command = self._importDataPopup)
        self.IMPORTDATA.grid(row = 0, column = 13)

        '''
        # Testing window size
        def get_size():
            w = root.winfo_width()
            h = root.winfo_height()
            print "CURRENTLY ... Width: {} ... Height: {}".format(w, h)
            print "REQUESTING ... Width: {} ... Height: {}".format(
                root.winfo_reqwidth(), root.winfo_reqheight())
            print "MAXIMUMS: {}".format(root.maxsize())

        self.btn = tk.Button(self, text="Window Size", command=get_size)
        self.btn.grid(row=0, column=14)
        '''

        self._setupEntryWidgets()
        self.setStatus("Welcome")

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
        import Query
        CashflowDB = Query.Query()
        query = ("SELECT contributionRates, bow, growth, yield, investYears, life, investStartDate "
                 "FROM Fund WHERE fundID = \'{}\'".format(self.fundNameTEXT.get()))
        result = CashflowDB.queryDB(query).fetchone()
        commitmentQuery = "SELECT capitalCommited(\'{}\')".format(self.fundNameTEXT.get())
        commitmentResult = CashflowDB.queryDB(commitmentQuery).fetchone()[0]
        if (result is None):
            self.setStatus("Invalid fund name!")
            return True
        print commitmentResult
        self.setEntryText(self.capitalCommitmentTEXT, str(commitmentResult))
        self.setEntryText(self.contributionRatesTEXT, result[0])
        self.setEntryText(self.bowTEXT, result[1])
        self.setEntryText(self.growthRateTEXT, result[2])
        self.setEntryText(self.fundYieldTEXT, result[3])
        self.setEntryText(self.lastInvestmentYearTEXT, result[4])
        self.setEntryText(self.lifeOfFundTEXT, result[5])
        startDate = result[6].date()
        self.setEntryText(self.startDateTEXT, "{}-{}-{}".format(str(startDate.year)[2:], startDate.month, startDate.day))

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
        pass

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
            self._popupWindow("Export Menu", "Export File As (.csv extension is already included):", "Confirm Export", self._exportModel)

    # Exports the model to a csv file
    def _exportModel(self, widget, fileName):
        self.fundModel.exportToCsv("{}.csv".format(fileName))
        if widget is not None:
            widget.destroy()
        self.setStatus("Saved {}.csv".format(fileName))

    # Exports all fund stats to a csv file called fundStats.csv
    def _exportFundStats(self):
        today = datetime.date.today()
        dateAsString = today.strftime("%y/%m/%d")
        fundStats = Output.Output()
        fundStats.exportOutput("fundStats.csv", dateAsString)
        self.setStatus("Fund stats exported to fundStats.csv")

    # Brings up a pop-up to prompt user for a file to read for export.
    # The file should be an excel sheet with fund codes listed all in the first column.
    def _massExportPopup(self):
        self._popupWindow("Mass Export Menu", "Read from (.xlsx extention is already included): ", "Confirm Mass Export", self._massExport)

    # Creates a simple popup window with a text box, entry box, execute box, and cancel box.
    # Reads the argument from the entry box when executing the command.
    def _popupWindow(self, title, message, executeButtonLabel, executeButtonCommand):
        top = tk.Toplevel()
        top.title(title)
        text = tk.Message(top, text=message)
        text.pack()
        fileEntry = tk.Entry(top)
        fileEntry.pack()
        confirmButton = tk.Button(top, text=executeButtonLabel, command=lambda: executeButtonCommand(top, fileEntry.get()))
        confirmButton.pack()
        cancelButton = tk.Button(top, text="Cancel", command=top.destroy)
        cancelButton.pack()

    # Executes the export of the funds in the given file, exporting in the order of Base, Actuals, Base+Actuals
    def _massExport(self, widget, fileName):
        try:
            fundCodeDf = pd.read_excel(ospath("{}.xlsx".format(fileName)), header=None)
        except IOError:
            widget.destroy()
            self.setStatus("Unable to find excel file!")
            return

        fundCount = 0
        for row in fundCodeDf.iterrows():
            fundCode = row[1][0]
            self.setEntryText(self.fundNameTEXT, fundCode)
            fillInputError = self._fillInputs()
            if fillInputError is True:
                continue
            for periodLength in ModelPeriod.ModelPeriod:
                self.setEntryText(self.segmentsTEXT, periodLength.value)
                for type in range(0, 3):
                    self.MODELTYPE.set(type)
                    self._createModel()
                    self._exportModel(None, fundCode)

            fundCount += 1

        widget.destroy()
        self.setStatus("{} fund files exported".format(fundCount))

    # Creates a popup window to prompt user for where to read data from.
    def _importDataPopup(self):
        self._popupWindow("Import Data Menu", "Read from (.xlsx extention is already included): ",
                            "Confirm Data Import", self._importData)

    # Imports (client, sponsor, fund, raw) data from the given file name.
    def _importData(self, widget, fileName):
        # ~/Box Sync/Shared/Lock-up Fund Client Holdings & Performance Tracker/Cash Flow Model/CBA Cash Flow Model - v2.17 Clearspring Analysis.xlsx
        if not os.path.exists('/Users/Whit/Box Sync/Shared/Lock-up Fund Client Holdings & Performance Tracker/Cash Flow Model/{}.xlsx'.format(fileName)):
            widget.destroy()
            self.setStatus("Unable to find excel file!")
            return

        validationReader = ValidationReader.ValidationReader(fileName)
        validationReader.processAll()
        # todo import raw data info
        widget.destroy()
        self.setStatus("Data imported")

    # Deletes all data from the database
    def _resetData(self):
        # todo
        pass

    # Sets the status of the GUI to the STATUS label.
    # Also adjusts the GUI to the requested size.
    def setStatus(self, status):
        self.STATUS["text"] = status

        root.update_idletasks()
        print "ROOT WIDTH 1 : {}".format(root.winfo_reqwidth())
        root.maxsize(width=root.winfo_reqwidth(), height=root.winfo_reqheight())
        root.geometry("{}x{}".format(root.winfo_reqwidth(), root.winfo_reqheight()))
        print "ROOT WIDTH 2 : {}".format(root.winfo_reqwidth())

    # Replaces any text in a given entry with the given text.
    def setEntryText(self, entry, text):
        entry.delete(0, tk.END)
        entry.insert(0, text)

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()


root = tk.Tk()

# inherits tk.Frame
app = Application(master=root)

app.mainloop()
root.destroy()