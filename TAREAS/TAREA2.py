import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from reportlab.graphics.samples.excelcolors import backgroundGrey

ventana = tk.Tk()
ventana.Label("CALCULADORA DE PROMEDIOS",font=("Arial", 12),).pack(pady=10)
ventana.geometry("600x600")
ventana.resizable(width=False, height=False)




titulo = tk.Label(ventana, text="CALCULADORA DE PROMEDIOS",font=("Arial", 25))
titulo.pack(pady=10)

tk.Label(ventana, text= "Parcial1",padx=10,pady=10).pack(pady=10)
tk.Label(ventana, text= "Parcial2", padx=10,pady=10).pack(pady=10)
tk.Label(ventana, text= "Parcial3", pady=10).pack(pady=10)
tk.Label(ventana, text= "Proyecto", padx=10,pady=10).pack(pady=10)

entry1=tk.Entry(ventana)
entry2=tk.Entry(ventana)
entry3=tk.Entry(ventana)
entry1.pack()
entry2.pack()
entry3.pack()


def Calcular_promedio():
    try:
        cal1=float(entry1.get())
        cal2=float(entry2.get())
        cal3=float(entry3.get())

        promedio = cal1+cal2+cal3 / (3)
        resultado_label.config(text=f"Promedio: {promedio:.2f}")
    except ValueError:
        messagebox.showerror("Error, datos faltantes")

# Botón
calcular_btn = tk.Button(ventana, text="Calcular Promedio", command=Calcular_promedio)
calcular_btn.pack(pady=10)

# Resultado
resultado_label = tk.Label(ventana, text="Promedio: ", font=("Arial", 12))
resultado_label.pack(pady=10)

# Ejecutar
ventana.mainloop()