from tkinter import *
from tkinter import ttk

root=Tk()
frm= ttk.Frame(root,padding=20)
frm.grid()
ttk.Label(frm, text='Mira ').grid(row=0, column=0)
ttk.Button(frm, text="Mi dedo", command=root.destroy).grid(column=1,row=0)
root.mainloop()
