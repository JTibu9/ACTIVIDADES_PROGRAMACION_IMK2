#Ejercicio2 usando coordenadas
#04/02/26
import tkinter as tk
from tkinter import ttk

ventana= tk.Tk()
ventana.geometry("480x300")
ventana.title("Grid")
#Grid organizar filas y comlumnas (Como en excel)
#row= fila y column= columna

#fila 0
ttk.Label(ventana,text="nombre:").grid(row=0,column=0,pady=5,padx=5)
entrada_nombre= ttk.Entry(ventana,width=50)
entrada_nombre.grid(row=0,column=1,pady=5,padx=5)

ttk.Label(ventana,text="apellido:").grid(row=1,column=0,pady=5,padx=5)
entrada_apellido=ttk.Entry(ventana,width=50)
entrada_apellido.grid(row=1,column=1,pady=5,padx=5)

ttk.Label(ventana,text="carrera:").grid(row=2,column=0,pady=5,padx=5)
entrada_carrera= ttk.Entry(ventana,width=50)
entrada_carrera.grid(row=2,column=1,pady=5,padx=5)

def mostrar_datos():
    nombre = entrada_nombre.get()
    apellido = entrada_apellido.get()
    carrera = entrada_carrera.get()
    print(f"{nombre},{apellido},{carrera}")
    if(nombre=="" or apellido=="" or carrera==""):
        etiqueta_error= ttk.Label(ventana,text="DATOS FALTANTES",background="red",foreground="white")
        etiqueta_error.grid(row=4,column=0,pady=5,padx=5)
    else:
        etiqueta_Bien= ttk.Label(ventana,text="DATOS COMPLETADOS",background="green",foreground="white")
        etiqueta_Bien.grid(row=4,column=0,pady=5,padx=5)


ttk.Button(ventana,text="Enviar",command=mostrar_datos).grid(row=3,column=0,pady=5,padx=5)

ventana.mainloop()