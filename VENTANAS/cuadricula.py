import tkinter as tk
from tkinter import ttk

ventana = tk.Tk()
ventana.title("Ejemplo direccion de botones")
ventana.geometry("600x480")

boton1= ttk.Button(ventana,text= "Boton1")
boton1.pack(side="left", pady=10, padx=10)

boton2= ttk.Button(ventana,text= "Boton2")
boton2.pack(side="left", pady=10, padx=10)

boton3= ttk.Button(ventana,text= "Derecha")
boton3.pack(side="left", pady=10, padx=10)

ventana.mainloop()