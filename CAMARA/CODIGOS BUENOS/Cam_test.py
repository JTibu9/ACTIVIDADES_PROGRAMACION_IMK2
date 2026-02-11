import cv2
import tkinter as tk
import serial
from tkinter import ttk
from PIL import Image, ImageTk

ventana = tk.Tk()
ventana.title("Camara")
ventana.geometry("400x680")

cap = None

video_lab = ttk.Label(ventana)
video_lab.grid(column=4, row=5)


def cam_video():
    global cap
    if cap is not None and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)

            # ✅ UNA sola conversión
            imgtk = ImageTk.PhotoImage(image=img)

            # ✅ Guardar referencia y mostrar
            video_lab.imgtk = imgtk
            video_lab.configure(image=imgtk)

        video_lab.after(10, cam_video)


def cam_inicialize():
    global cap
    if cap is None:
        cap = cv2.VideoCapture(0)
        cam_video()


def cam_stop():
    global cap
    if cap is not None:
        cap.release()
        cap = None
        video_lab.config(image="")


boton = ttk.Button(ventana, text="Camara", command=cam_inicialize, width=20)
boton.grid(column=4, row=6)

boton2 = ttk.Button(ventana, text="Detener camara", command=cam_stop, width=20)
boton2.grid(column=5, row=6)

ventana.mainloop()
