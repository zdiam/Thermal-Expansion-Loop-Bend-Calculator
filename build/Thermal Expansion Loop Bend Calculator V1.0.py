import tkinter as tk
from tkinter import *
import pandas as pd
from PIL import ImageTk, Image
from tkinter import filedialog
#start of input gui
root = Tk()
root.geometry('1200x1200')
root.title('Thermal Expansion Calculator')
root.resizable(width=False, height=False)

#image from folder
x = 'steel pipe data.png'
img = Image.open(x)
img = img.resize((800, 1150))
img = ImageTk.PhotoImage(img)
panel = Label(root, image=img)
panel.image = img
panel.pack(side=RIGHT)



def info():
    list_of_lists = [[f'{psig.get()}',],
                    [f'{length.get()}',], [f'{pipeOD.get()}',]],


entry1_text = Label(root, text = 'Enter Pressure of Steam(psig)')
entry2_text = Label(root, text = 'Enter Straight Length of Pipe(ft)')
entry3_text = Label(root, text = 'Enter Outside Diameter of Pipe(in^2)')
creditText = Label(root, text = 'Credit to 2016 ASHRAE Handbook—HVAC Systems and Equipment Chapter 46')
#edit credit?
entry1_text.place(x = 15, y = 30)
entry2_text.place(x = 15, y = 90)
entry3_text.place(x = 15, y = 150)
creditText.place(x=395, y=1175)

psig = StringVar()
length = StringVar()
pipeOD = StringVar()


psig_entry = Entry(root, textvariable = psig, width = "15")
length_entry = Entry(root, textvariable = length, width = "15")
pipeOD_entry = Entry(root, textvariable = pipeOD, width = "15")

psig_entry.place(x = 15, y = 60)
length_entry.place(x = 15, y = 120)
pipeOD_entry.place(x=15, y = 180)


register = Button(root,text = "Run", width = "10", height = "2", command=root.destroy, bg = "#32a86d")
register.place(x = 15, y = 240)

root.mainloop()
#end of input gui

from pyXSteam.XSteam import XSteam







psigC = float(psig.get())
lengthC = float(length.get())
psia = psigC + 14.696
#add atm to psig of steam for psia steam tables

steamTable = XSteam(XSteam.UNIT_SYSTEM_FLS)


tempPsi = steamTable.tsat_p(psia)
tempPsi


#https://www.engineeringtoolbox.com/pipes-temperature-expansion-coefficients-d_48.html

#10-6 in/in oF
#Aluminum	12.8	
#Carbon Steel	6.5	
#Cast Iron	5.9	
#Copper	9.3	
#Stainless Steel	9.9	
#ABS Acrylonitrile butadiene styrene	35.0	
#HDPE High density polyethylene	67.0	
#PE Polyethylene	83.0	
#CPVC Chlorinated polyvinyl chloride	44.0	
#PVC Polyvinyl chloride	28.0	

#typically carbon steel for steam but added for reference in future


coeffTExp = 6.5 * 10**-6
deltaExp = coeffTExp * lengthC * tempPsi * 12#(in conversion) 
deltaExp

pipeODC = float(pipeOD.get())

import math
deltaPSq = math.sqrt(deltaExp*pipeODC)

zL = 4 *deltaPSq

uL = 6.225 * deltaPSq

uW = (uL/5)
uH = 2*uW
#zL,uL,uW and uH calcs are from ASHRAE as accepted standard and reference

zLT = str(round(zL, 2))
uLT = str(round(uL, 2))
uWT = str(round(uW, 2))
uWH = str(round(uH, 2))
#for better appearance in output gui


#start of output gui
root = Tk()
root.geometry('800x400')
root.title('Thermal Expansion Output Values')

root.resizable(width=False, height=False)

#image from folder
y = 'z bend and loop.png'
img = Image.open(y)
img = img.resize((500, 350))
img = ImageTk.PhotoImage(img)
panel = Label(root, image=img)
panel.image = img
panel.pack(side=RIGHT)



entry1_text = Label(root, text = 'Z-bend length is : ' + zLT + ' ft.')
entry2_text = Label(root, text = 'Expansion total loop length is : ' + uLT+ ' ft.')
entry3_text = Label(root, text = 'Expansion loop width is : ' + uWT+ ' ft.')
entry4_text = Label(root, text = 'Expansion loop height is : ' + uWH+ ' ft.')

creditText2 = Label(root, text = 'Credit to 2016 ASHRAE Handbook—HVAC Systems and Equipment Chapter 46')

ztext = '\u0332'.join('Z-Bend Reference Image'+' ')[:-1]
ltext = '\u0332'.join('Expansion Loop Reference Image'+' ')[:-1]
#this is to underline and highlight the titles from the image
zbend_text = Label(root, text = ztext)
eloop_text = Label(root, text = ltext)


entry1_text.place(x = 15, y = 30)
entry2_text.place(x = 15, y = 90)
entry3_text.place(x = 15, y = 150)
entry4_text.place(x = 15, y = 210)

creditText2.place(x=295, y=375)

zbend_text.place(x=485,y=5)
eloop_text.place(x=465,y=200)

#start of building the filename
from datetime import date
today = date.today()
today
#dataframe for excel output
df = pd.DataFrame({'Expansion Type': ['Z-bend length', 'Expansion total loop length', 'Expansion loop width','Expansion loop height'], 'Value (ft.)' : [zLT, uLT, uWT,uWH]})
psigP= psig.get()
lengthP = length.get()

filepath = ( (str(today))+'_'+psigP +'PSI'+'_'+lengthP+'Length'+'.csv')



registerPrint = Button(root,text = "Print!", width = "25", height = "3", command=df.to_csv (filepath,index=None), bg = "#1FE9EB")
registerPrint.place(x = 15, y = 270)
#it may be ideal to make a combined function to have the print button close in the future rather than two seperate buttons
registerClose = Button(root,text = "Close", width = "15", height = "2", command=root.destroy)
registerClose.place(x = 15, y = 330)

root.mainloop()
#end of output gui

#end of program
