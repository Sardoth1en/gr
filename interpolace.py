import pylab as pl
import scipy.interpolate as inp
x= [0, 0.3, 0.5, 0.8, 1,  2,  3 ]
y= [0, 0.1, 0.5, 1,   3, 10, 30]

#x= "0 0.3 0.5 0.8 1  2  3".split()
#y= "0 0.1 0.5 1   3 10 30".split()

#x=list(map(float,x))


funkce = inp.CubicSpline(x,y)
newX= pl.linspace(0,3,99)
newY=funkce(newX)

pl.plot(newX,inp.Akima1DInterpolator(x,y)(newX),label= "akima")
pl.plot(newX,inp.PchipInterpolator(x,y)(newX),label= "pchip")
pl.plot(newX,inp.UnivariateSpline(x,y)(newX),label= "UnivariateSpline")
pl.plot(x,y, "ro", label= "původní hodnoty")
pl.plot(newX,newY, label= "cubic spline")
pl.legend()
pl.grid()
pl.show()