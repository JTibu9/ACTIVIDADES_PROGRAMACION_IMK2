import tkinter as tk
from tkinter import ttk

ventana= tk.Tk()
ventana.geometry("400x300")
ventana.title("Sistema de Monitoreo-Principal")

#Variables Globales
#Estas variables nos van a servir para compartir datos

temperatura_actual = tk.StringVar()
temperatura_actual.set("")

#ventana principal
##Etiqueta

ttk.Label(
    ventana,
    text="Temperatura actual",
    font=("Times New Roman",20)
).pack(pady=10)
#La etiqueta se va a estar actualizando de manera automatica
#Cuando
Label_temperatura=ttk.Label(
    ventana,
    textvariable=temperatura_actual, #Se conecta a la variable
    font=("Times New Roman",20),
)
Label_temperatura.pack(pady=10)
ttk.Label(ventana,text="°C").pack()

def abrir_configuracion():
    #Crear la ventana secundaria
    ventana_config= tk.Toplevel()
    ventana_config.title("Configuracion")
    ventana_config.geometry("300x200")
    
    ttk.Label(
        ventana_config,
        text="Ingresa la temperatura actual",
        font=("Times New Roman",20)).pack(pady=10)

    entry_temp= ttk.Entry(ventana_config,textvariable=temperatura_actual)
    entry_temp.pack(pady=10)

#Funcion para estar actualizando el valor
    def guardar():
        #Obtememos La variable de entrada
        nuevo_valor= entry_temp.get()
        #Actualizar la variable global
        temperatura_actual.set(nuevo_valor)
        #Cerrar la ventana configuracion
        ventana_config.destroy()

    ttk.Button(
        ventana_config,
        text="Guardar",
        command=guardar
    ).pack(pady=10)

#Boton para abrir configuracion
ttk.Button(
    ventana,
    text="Abrir",
    command=abrir_configuracion
).pack(pady=10)


ventana.mainloop()
