import pylab as pl
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog


#messagebox.showerror("Titulek", "Nefunguje to")

#odpoved  = messagebox.askyesno("TItilek", "Chceš to")

#print(odpoved)

#filedialog.askopenfile(title="otevči", initialdir=".")



class Application(tk.Tk):
    #name = basename(splitext(basename(__file__.capitalize()))[0])      Nastavuje jméno z názvu souboru
    name = "Grafy POG"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)
        self.lbl = tk.Label(self, text="Grafování")
        self.lbl.pack()
        self.Quitbtn = tk.Button(self, text="Quit", command=self.quit)
        self.zpracbtn = tk.Button(self, text="zpracuj", command=self.zpracuj)
        self.veberbtn = tk.Button(self, text= "Vyber soubor", command=self.vyber)
        self.veberbtn.pack()
        self.zpracbtn.pack()
        self.Quitbtn.pack()
        

    def quit(self, event=None):
        super().quit()

    def vyber(self):
        self.filename = filedialog.askopenfilename(title="otevči", initialdir="/home/public")

    
    def zpracuj(self):
        if not self.filename:
            return
        axisx = []
        axisy= []
        with open(self.filename, "r") as f:
            while line := f.readline():
                x, y = line.split()
                axisx.append(float(x))
                axisy.append(float(y))
            pl.plot(axisx,axisy,color = "#123456", linestyle= "dashdot")
            if self.filename == "/home/public/graf.txt":
                pl.title("Kardinální sinus")
            else:
                pl.title("Graf")
            pl.grid()
            pl.show()



app = Application()
app.mainloop()

#helli