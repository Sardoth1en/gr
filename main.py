from os.path import basename, splitext
import tkinter as tk
from tkinter import filedialog
import pylab as pl
import scipy.interpolate as inp
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
    colors = ("black","red","white","yellow","magenta","cyan","gree","blue")

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

       

        self.grafFrame= tk.LabelFrame(self, text="Graf")
        self.grafFrame.pack(padx=5,pady=5,fill ="x")

        tk.Label(self.grafFrame, text="Titulek").grid(row=0,column=0)

        self.titleEntry= MyEntry(self.grafFrame)
        self.titleEntry.grid(row=0 , column=1)

        tk.Label(self.grafFrame, text="Osa x").grid(row=1,column=0)

        self.xlabelEntry= MyEntry(self.grafFrame)
        self.xlabelEntry.grid(row=1 , column=1,columnspan=2)

        tk.Label(self.grafFrame, text="Osa y").grid(row=2,column=0)

        self.ylabelEntry= MyEntry(self.grafFrame)
        self.ylabelEntry.grid(row=2 , column=1,columnspan=2)

        self.plotBtn = tk.Button(self, text="Kresli", command=self.plot)
        self.plotBtn.pack(anchor="e",fill="x")

        tk.Label(self.grafFrame, text="styl čáry").grid(row=3,column=0)
        self.lineVar= tk.StringVar(value="none")
        tk.OptionMenu(self.grafFrame, self.lineVar, "none", ":","-.","--","-").grid(row=3,column=1,sticky="w")

        self.colorVar= tk.StringVar(value="none")
        tk.OptionMenu(self.grafFrame, self.colorVar, *self.colors).grid(row=3,column=2,sticky="w")

        tk.Label(self.grafFrame, text="marka").grid(row=4,column=0)
        self.markVar= tk.StringVar(value="none")
        tk.OptionMenu(self.grafFrame, self.markVar, "none", *tuple(".,<>vo+pxX*1234")).grid(row=4,column=1,sticky="w")
        self.mcolorVar= tk.StringVar(value="none")
        tk.OptionMenu(self.grafFrame, self.mcolorVar, *self.colors).grid(row=4,column=2,sticky="w")

        self.gridVar = tk.BooleanVar(value=True)
        tk.Label(self.grafFrame, text="Mřížka").grid(row=5,column=0)
        tk.Checkbutton(self.grafFrame, variable=self.gridVar ).grid(row=5,column=1,sticky="w")

        tk.Label(self.grafFrame, text="interpolace").grid(row=6,column=0)
        self.ilineVar= tk.StringVar(value="none")
        tk.OptionMenu(self.grafFrame, self.ilineVar, "none", "CubicSpline","PchipInterpolator","Akima1DInterpolator","UnivariateSpline").grid(row=6,column=1,sticky="w")

        self.icolorVar= tk.StringVar(value="none")
        tk.OptionMenu(self.grafFrame, self.icolorVar, *self.colors).grid(row=6,column=2,sticky="w")

        self.btn = tk.Button(self, text="Quit", command=self.quit)
        self.btn.pack()


        #self.mainMenu = tk.Menu(self)
        #self.fileMenu = tk.Menu(self.mainMenu)
        #self.editMenu = tk.Menu(self.mainMenu)
        #self.helpMenu = tk.Menu(self.mainMenu)
        #self.config(menu=self.mainMenu)

        #self.mainMenu.add_cascade(Label= "Soubor" , menu=self.fileMenu)
       # self.mainMenu.add_cascade(Label= "Editovat" , menu=self.editMenu)
        #self.mainMenu.add_cascade(Label= "Napoveda" , menu=self.helpMenu)

        #self.fileMenu.add_command(label="otevřít", command= self.choseFile)
        #self.fileMenu.add_separator()
        #self.fileMenu.add_command(label="konec", command=self.quit)

        #self.editMenu.add_cascade(label="ovoce",menu=self.ovoce)
        #self.editMenu.add_cascade(label="zelenina",menu=self.zelenina)


        #self.ovovce.add_command(label="višen")
        #self.ovovce.add_command(label="jablko")
        #self.ovovce.add_command(label="hruška")
        #self.ovovce.add_command(label="malina")


        #self.zelenina.add_checkbutton(label="mrkev")


    def choseFile(self):
        path = filedialog.askopenfilename()
        self.fileEntry.value = path
        self.fileEntry.xview_moveto(1)

    def plot(self):
        with open(self.fileEntry.value) as f:
            if self.dataVar.get() == "row":
                line = f.readline()
                x= line.split(";")
                line = f.readline()
                y= line.split(";")
                x = [ float(item.replace(",",".")) for item in x]
                y = [ float(item.replace(",",".")) for item in y]
            if self.dataVar.get() == "column":
                x = []
                y = []
                while True:
                    line = f.readline()
                    if line == "":
                        break
                    if ";" not in line:
                        continue
                    x1,y1 = line.split(";")
                    x.append(float(x1.replace(",",".")))
                    y.append(float(y1.replace(",",".")))
            
            if self.ilineVar.get() != "none":
                x_min = min(x)
                x_max = max(x)
                xx = pl.linspace(x_min,x_max)
                if self.ilineVar.get() == "CubicSpline":  
                    funkce = inp.CubicSpline(x,y)
                    yy = funkce(xx)
                    pl.plot(xx,yy,color=self.icolorVar.get())
                if self.ilineVar.get() == "PchipInterpolator":
                    funkce = inp.PchipInterpolator(x,y)
                    yy = funkce(xx)
                    pl.plot(xx,yy,color=self.icolorVar.get())
                if self.ilineVar.get() == "Akima1DInterpolator":
                    funkce = inp.Akima1DInterpolator(x,y)
                    yy = funkce(xx)
                    pl.plot(xx,yy,color=self.icolorVar.get())
                if self.ilineVar.get() == "UnivariateSpline":
                    funkce = inp.UnivariateSpline(x,y)
                    yy = funkce(xx)
                    pl.plot(xx,yy,color=self.icolorVar.get())
                
            pl.grid(self.gridVar.get())
            pl.plot(x,y,linestyle=self.lineVar.get(),marker=self.markVar.get(),color=self.colorVar.get(),markeredgecolor=self.mcolorVar.get(),markerfacecolor=self.mcolorVar.get())
            pl.title(self.titleEntry.value)
            pl.xlabel(self.xlabelEntry.value)
            pl.ylabel(self.ylabelEntry.value)
            
            pl.show()

    def about(self):
        window = About(self)
        window.grab_set()

    def quit(self, event=None):
        super().quit()


app = Application()
app.mainloop()