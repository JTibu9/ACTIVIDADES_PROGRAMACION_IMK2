import serial
import tkinter as tk
import cv2

cap = cv2.VideoCapture(0)
# 🔧 CONFIGURACIÓN SERIAL
PUERTO = "/dev/ttyUSB0"  # cambia si es necesario
BAUDIOS = 9600

try:
    arduino = serial.Serial(PUERTO, BAUDIOS, timeout=1)
except:
    print("❌ No se pudo abrir el puerto serial")
    exit()

# 🪟 Ventana principal
ventana = tk.Tk()
ventana.title("Sensor DHT11")
ventana.geometry("300x200")

# Labels
lbl_temp = tk.Label(ventana, text="Temperatura: -- °C", font=("Arial", 14))
lbl_temp.pack(pady=10)

lbl_hum = tk.Label(ventana, text="Humedad: -- %", font=("Arial", 14))
lbl_hum.pack(pady=10)

lbl_tempF= tk.Label(ventana, text="Temperatura Farenheit: -- °F", font=("Arial", 14))
lbl_tempF.pack(pady=10)


def leer_serial():
    if arduino.in_waiting:
        linea = arduino.readline().decode("utf-8").strip()

        if linea.startswith("TEMP"):
            try:
                datos = linea.split(",")
                temp = datos[0].split(":")[1]
                hum = datos[1].split(":")[1]
                tempF = datos[2].split(":")[1]

                lbl_temp.config(text=f"Temp: {temp} °C")
                lbl_hum.config(text=f"Hum: {hum} %")
                lbl_tempF.config(text=f"Temp Farenheit: {tempF} °F")
            except:
                pass

    ventana.after(1000, leer_serial)
# Iniciar lectura
leer_serial()
ventana.mainloop()
