import serial
import time
import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import collections

# ---------------- CONFIG ----------------
PUERTO = "/dev/ttyUSB0"
BAUDIOS = 9600
MUESTRAS = 60

# ---------------- CLASE PRINCIPAL ----------------
class AppTermicaDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Térmico + Sensores")
        self.root.geometry("1100x750")
        # -------- Serial --------
        try:
            self.ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)
            time.sleep(2)
            print("Arduino conectado")
        except:
            self.ser = None
            print("No se pudo abrir el puerto")

        # -------- Datos --------
        self.temp_actual = 25.0
        self.temp_data = collections.deque([0]*MUESTRAS, maxlen=MUESTRAS)
        self.dist_data = collections.deque([0]*MUESTRAS, maxlen=MUESTRAS)

        # -------- Cámara --------
        self.cap = cv2.VideoCapture(0)

        # -------- Notebook --------
        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.tab_cam = ttk.Frame(notebook)
        self.tab_graf = ttk.Frame(notebook)

        notebook.add(self.tab_cam, text="Cámara Térmica")
        notebook.add(self.tab_graf, text="Gráficas")

        # ================= TAB CÁMARA =================
        self.lbl_video = tk.Label(self.tab_cam)
        self.lbl_video.pack(pady=10)

        self.lbl_info = tk.Label(
            self.tab_cam,
            text="Temperatura: -- °C",
            font=("Arial", 14)
        )
        self.lbl_info.pack()

        # ================= TAB GRÁFICAS =================
        self.fig = Figure(figsize=(8, 5), dpi=100)

        self.ax_temp = self.fig.add_subplot(211)
        self.ax_temp.set_title("Temperatura Ambiente (°C)")
        self.ax_temp.set_ylim(0, 50)
        self.ax_temp.grid(True)

        self.ax_dist = self.fig.add_subplot(212)
        self.ax_dist.set_title("Distancia Ultrasónica (cm)")
        self.ax_dist.set_ylim(0, 100)
        self.ax_dist.grid(True)

        self.line_temp, = self.ax_temp.plot([], [], 'r', linewidth=2)
        self.line_dist, = self.ax_dist.plot([], [], 'b', linewidth=2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab_graf)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # -------- Loops --------
        self.actualizar_serial()
        self.actualizar_camara()

    # ---------- MAPEO TEMP ----------
    def temp_a_escala(self, temp, t_min=15, t_max=40):
        temp = max(t_min, min(t_max, temp))
        return int(255 * (temp - t_min) / (t_max - t_min))

    # ---------- PARSER SERIAL ----------
    def parsear_linea(self, linea):
        temp = None
        dist = None

        try:
            if "TEMP:" in linea:
                temp = float(linea.split("TEMP:")[1].split(",")[0])
            if "Distancia" in linea:
                dist = float(linea.split("Distancia de objetos:")[1])
        except:
            pass

        return temp, dist

    # ---------- CÁMARA ----------
    def actualizar_camara(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gris = cv2.add(gris, self.temp_a_escala(self.temp_actual))
                termico = cv2.applyColorMap(gris, cv2.COLORMAP_JET)
                termico = cv2.cvtColor(termico, cv2.COLOR_BGR2RGB)

                img = Image.fromarray(termico)
                imgtk = ImageTk.PhotoImage(image=img)
                self.lbl_video.imgtk = imgtk
                self.lbl_video.configure(image=imgtk)

        self.root.after(20, self.actualizar_camara)

    # ---------- SERIAL + GRÁFICAS ----------
    def actualizar_serial(self):
        if self.ser and self.ser.in_waiting:
            try:
                linea = self.ser.readline().decode().strip()
                temp, dist = self.parsear_linea(linea)

                if temp is not None:
                    self.temp_actual = temp
                    self.temp_data.append(temp)
                    self.lbl_info.config(text=f"Temperatura: {temp:.1f} °C")

                if dist is not None:
                    self.dist_data.append(dist)

                x = range(len(self.temp_data))

                self.line_temp.set_data(x, self.temp_data)
                self.ax_temp.set_xlim(0, MUESTRAS)

                self.line_dist.set_data(x, self.dist_data)
                self.ax_dist.set_xlim(0, MUESTRAS)

                self.canvas.draw_idle()

            except:
                pass

        self.root.after(300, self.actualizar_serial)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AppTermicaDashboard(root)
    root.mainloop()
