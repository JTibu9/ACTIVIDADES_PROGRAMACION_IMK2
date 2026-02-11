import tkinter as tk
#Agregado de tk
from tkinter import ttk


ventana = tk.Tk()
ventana.geometry("300x300")
ventana.title("Pepe")
ventana.resizable(False,False)
ventana.config(background='#606173')

#Crear etiqueta
etiqueta = ttk.Label(ventana, text='Saludos')
#Cambiar el texto
etiqueta.config(text="Nos vemos")
#Publicar etiqueta
etiqueta.pack(pady=10)
etiqueta["text"]="Adios"


ventana.mainloop()

