import serial
import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

# ------------------ CONFIGURACIÓN SERIAL ------------------
PUERTO = "/dev/ttyUSB0"  # cambia si es necesario
BAUDIOS = 9600

try:
    arduino = serial.Serial(PUERTO, BAUDIOS, timeout=1)
except:
    print("❌ No se pudo abrir el puerto serial")
    exit()

# ------------------ CÁMARA ------------------
cap = cv2.VideoCapture(0)
# ------------------ VENTANA ------------------
ventana = tk.Tk()
ventana.title("Sensores + Cámara")
filtro = tk.StringVar(value="Normal")
ventana.geometry("500x600")
# ------------------ LABEL VIDEO ------------------
lbl_video = tk.Label(ventana)
lbl_video.pack(pady=10)
#-------------------FILTRO-------------------------
ttk.Label(ventana,text="Filtro de camara").pack()
combo_filtro= ttk.Combobox(ventana,textvariable=filtro,values=["Normal","Grises","Termico"],state="readonly", width=15)
combo_filtro.pack(pady=5)


# ------------------ LABELS SENSOR ------------------
lbl_temp = tk.Label(ventana, text="Temperatura: -- °C", font=("Arial", 12))
lbl_temp.pack(pady=5)

lbl_hum = tk.Label(ventana, text="Humedad: -- %", font=("Arial", 12))
lbl_hum.pack(pady=5)

lbl_tempF = tk.Label(ventana, text="Temperatura Fahrenheit: -- °F", font=("Arial", 12))
lbl_tempF.pack(pady=5)

# ------------------ FUNCIÓN CÁMARA ------------------
def mostrar_camara():
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Aplicar filtros
            if filtro.get() == "Grises":
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)

            elif filtro.get() == "Térmico":
                gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.applyColorMap(gris, cv2.COLORMAP_JET)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            else:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            lbl_video.imgtk = imgtk
            lbl_video.configure(image=imgtk)

    lbl_video.after(10, mostrar_camara)

# ------------------ FUNCIÓN SERIAL ------------------
def leer_serial():
    if arduino.in_waiting:
        linea = arduino.readline().decode("utf-8").strip()

        if linea.startswith("TEMP"):
            try:
                datos = linea.split(",")
                temp = datos[0].split(":")[1]
                hum = datos[1].split(":")[1]
                tempF = datos[2].split(":")[1]

                lbl_temp.config(text=f"Temperatura: {temp} °C")
                lbl_hum.config(text=f"Humedad: {hum} %")
                lbl_tempF.config(text=f"Temperatura Fahrenheit: {tempF} °F")
            except:
                pass

    ventana.after(1000, leer_serial)

# ------------------ INICIAR ------------------
mostrar_camara()
leer_serial()
ventana.mainloop()

# ------------------ LIBERAR RECURSOS ------------------
cap.release()
arduino.close()
