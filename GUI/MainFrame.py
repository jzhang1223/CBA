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
    '''
        self.FUNDNAME = tk.Entry(self)

        self.FUNDNAME.pack({"side": "left"})

        self.SUBMIT = tk.Button(self)
        self.SUBMIT["text"] = "SUBMIT"
        self.SUBMIT["command"] = self.saveData
        self.SUBMIT.pack({"side": "left"})
        '''

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

        self.fundModel = None #todo

    def saveData(self):
        print "saving data..."

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
root.destroy()