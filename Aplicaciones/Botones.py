import tkinter as tk
#Agregado de tk
from tkinter import ttk


ventana = tk.Tk()
ventana.geometry("300x300")
ventana.title("Pepe")
ventana.resizable(False,False)
ventana.config(background='#606173')

#funcion para click del boton
def saludar(nombre):
    print(f"{nombre},saludo")
#Creando el primer boton
boton1=ttk.Button(ventana,text="This is azerbayan virus",command=lambda:saludar("Yeezus"))
boton1.pack(side="top")



ventana.mainloop()