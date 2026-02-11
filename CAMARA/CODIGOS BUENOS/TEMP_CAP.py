import serial
import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk

# ------------------ CONFIG SERIAL ------------------
PUERTO = "/dev/ttyUSB0"
BAUDIOS = 9600

try:
    arduino = serial.Serial(PUERTO, BAUDIOS, timeout=1)
except:
    print("No se pudo abrir el puerto serial")
    exit()

# ------------------ CÁMARA ------------------
cap = cv2.VideoCapture(0)

# ------------------ VENTANA ------------------
ventana = tk.Tk()
ventana.title("Cámara térmica con DHT")
ventana.geometry("600x720")

# ------------------ VARIABLES ------------------
filtro = tk.StringVar(value="Normal")
temp_actual = 25.0  # valor inicial seguro

# ------------------ VIDEO ------------------
lbl_video = tk.Label(ventana)
lbl_video.pack(pady=10)

# ------------------ SELECTOR ------------------
ttk.Label(ventana, text="Modo de visualización").pack()
ttk.Combobox(
    ventana,
    textvariable=filtro,
    values=["Normal", "Térmico"],
    state="readonly",
    width=15
).pack(pady=5)

# ------------------ LABELS ------------------
lbl_temp = tk.Label(ventana, text="Temperatura: -- °C", font=("Arial", 12))
lbl_temp.pack()

lbl_hum = tk.Label(ventana, text="Humedad: -- %", font=("Arial", 12))
lbl_hum.pack()

# ------------------ FUNCIÓN MAPEO TEMP → COLOR ------------------
def temp_a_escala(temp, t_min=15, t_max=40):
    temp = max(t_min, min(t_max, temp))
    return int(255 * (temp - t_min) / (t_max - t_min))

# ------------------ FUNCIÓN CÁMARA ------------------
def mostrar_camara():
    global temp_actual

    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            if filtro.get() == "Térmico":
                gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Escalar brillo según temperatura DHT
                escala = temp_a_escala(temp_actual)
                gris = cv2.add(gris, escala)

                termico = cv2.applyColorMap(gris, cv2.COLORMAP_JET)

                # ----- Barra térmica -----
                barra = np.linspace(0, 255, 256).astype(np.uint8)
                barra = np.repeat(barra[:, np.newaxis], 30, axis=1)
                barra = cv2.applyColorMap(barra, cv2.COLORMAP_JET)

                h, w, _ = termico.shape
                termico[10:266, w-40:w-10] = barra

                frame = cv2.cvtColor(termico, cv2.COLOR_BGR2RGB)
            else:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            lbl_video.imgtk = imgtk
            lbl_video.configure(image=imgtk)

    lbl_video.after(20, mostrar_camara)

# ------------------ FUNCIÓN SERIAL ------------------
def leer_serial():
    global temp_actual

    if arduino.in_waiting:
        linea = arduino.readline().decode("utf-8").strip()

        if linea.startswith("TEMP"):
            try:
                datos = linea.split(",")
                temp_actual = float(datos[0].split(":")[1])
                hum = datos[1].split(":")[1]

                lbl_temp.config(text=f"Temperatura: {temp_actual:.1f} °C")
                lbl_hum.config(text=f"Humedad: {hum} %")
            except:
                pass

    ventana.after(1000, leer_serial)

# ------------------ INICIAR ------------------
mostrar_camara()
leer_serial()
ventana.mainloop()

cap.release()
arduino.close()
