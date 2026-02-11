import tkinter as tk
from tkinter import ttk

ventana = tk.Tk()
ventana.geometry ("400x300")
ventana.title("My GUI")

##Label que indica que escribir
etiqueta = ttk.Label(ventana, text="Escribe tu nombre: ")
etiqueta.pack(pady=10, padx=10)

##Entry es el campo donde el usuario escribe
entrada = ttk.Entry(ventana)
entrada.pack(pady=10)

def mostrar_nombre():
    nombre = entrada.get()
    print(f"nombre,{nombre}")


boton=ttk.Button(ventana,text="Mostrar", command=mostrar_nombre)
boton.pack(pady=10)
ventana.mainloop()