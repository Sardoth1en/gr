from os.path import basename, splitext
import tkinter as tk
from tkinter import filedialog
import pylab as pl
# from tkinter import ttk


class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        if not "textvariable" in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)


class About(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent, class_=parent.name)
        self.config()

        btn = tk.Button(self, text="Konec", command=self.close)
        btn.pack()

    def close(self):
        self.destroy()


class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "Foo"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)
        self.lbl = tk.Label(self, text="Hello World")
        self.lbl.pack()
        
        self.btn2 = tk.Button(self, text="About", command=self.about)
        self.btn2.pack()

        self.fileFrame= tk.LabelFrame(self, text="Soubor")
        self.fileFrame.pack(padx=5, pady=5, fill="x")
        self.fileEntry = MyEntry(self.fileFrame)
        self.fileEntry.pack(fill="x")
        self.fileBtn = tk.Button(self.fileFrame, text="...", command=self.choseFile)
        self.fileBtn.pack(anchor="e",fill="x")


        self.dataVar = tk.StringVar()
        self.rowRadio= tk.Radiobutton(self.fileFrame, text="Data jsou v řádcích", variable=self.dataVar, value="row")
        self.rowRadio.pack(anchor="w")
        self.columnRadio= tk.Radiobutton(self.fileFrame, text="Data jsou ve sloupcívh",variable=self.dataVar, value="column")
        self.columnRadio.pack(anchor="w")

        self.plotBtn = tk.Button(self, text="Kresli", command=self.plot)
        self.plotBtn.pack(anchor="e",fill="x")




        self.btn = tk.Button(self, text="Quit", command=self.quit)
        self.btn.pack()



    def choseFile(self):
        path = filedialog.askopenfilename()
        self.fileEntry.value = path

    def plot(self):
        with open(self.fileEntry.value) as f:
            if self.dataVar.get() == "row":
                line = f.readline()
                x= line.split(";")
                line = f.readline()
                y= line.split(";")
                x = [ float(item.replace(",",".")) for item in x]
                y = [ float(item.replace(",",".")) for item in y]
            pl.plot(x,y)
            pl.show()

    def about(self):
        window = About(self)
        window.grab_set()

    def quit(self, event=None):
        super().quit()


app = Application()
app.mainloop()