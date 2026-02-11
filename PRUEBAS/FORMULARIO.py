import tkinter as tk
from cProfile import label
from tkinter import ttk

from debian.debtags import output

ventana = tk.Tk()
ventana.geometry ("400x300")
ventana.configure(background="Yellow")
ventana.title("My GUI")

##Label que indica que escribir
etiqueta = ttk.Label(ventana, text="Escribe tu nombre: ")
etiqueta.pack(pady=10, padx=10)

##Entry es el campo donde el usuario escribe
entrada = ttk.Entry(ventana)
entrada_2=ttk.Entry(ventana)
entrada.pack(pady=10)
entrada_2.pack(pady=20)

def mostrar_nombre_apellido():
    nombre = entrada.get()
    apellido = entrada_2.get()
    salida = ttk.Label(ventana, text= f"Hola bro, {nombre} {apellido}")
    salida.pack(pady=40)


boton=ttk.Button(ventana,text="Saludar", command=mostrar_nombre_apellido)
boton.pack(pady=10)



ventana.mainloop()