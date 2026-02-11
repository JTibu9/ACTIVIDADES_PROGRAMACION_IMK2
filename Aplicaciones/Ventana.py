import tkinter as tk

ventana = tk.Tk()
#Redimensionar la ventana
ventana.geometry("300x300")
#Modificar el titulo
ventana.title("Pepe")

#funcion para no permitir el cambio de temaño
ventana.resizable(False,False)

#Cambiar el color del fondo de la ventana
ventana.config(background='#606173')
#Etiquetas

ventana.mainloop()

