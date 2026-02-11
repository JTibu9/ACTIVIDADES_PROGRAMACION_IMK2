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
PUERTO_1 = "/dev/ttyUSB0"   # TEMP + DIST
PUERTO_2 = "/dev/ttyUSB1"   # GIROSCOPIO
BAUDIOS = 9600
MUESTRAS = 60


class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard Multisensor + Cámara Térmica")
        self.root.geometry("1100x850")

        # -------- Serial --------
        self.ser1 = self.abrir_serial(PUERTO_1)
        self.ser2 = self.abrir_serial(PUERTO_2)

        # -------- Estado --------
        self.temp_actual = None   # ENTRADA PARA DATOS

        # -------- Buffers --------
        self.temp_data = collections.deque([0]*MUESTRAS, maxlen=MUESTRAS)
        self.dist_data = collections.deque([0]*MUESTRAS, maxlen=MUESTRAS)

        self.gx_data = collections.deque([0]*MUESTRAS, maxlen=MUESTRAS)
        self.gy_data = collections.deque([0]*MUESTRAS, maxlen=MUESTRAS)
        self.gz_data = collections.deque([0]*MUESTRAS, maxlen=MUESTRAS)

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

        self.lbl_temp = tk.Label(
            self.tab_cam,
            text="Temperatura: -- °C",
            font=("Arial", 14)
        )
        self.lbl_temp.pack()

        # ================= TAB GRÁFICAS =================
        self.fig = Figure(figsize=(9, 6), dpi=100)

        self.ax_temp = self.fig.add_subplot(311)
        self.ax_temp.set_title("Temperatura (°C)")
        self.ax_temp.set_ylim(0, 50)
        self.ax_temp.grid(True)
        self.line_temp, = self.ax_temp.plot([], [], 'r')

        self.ax_dist = self.fig.add_subplot(312)
        self.ax_dist.set_title("Distancia (cm)")
        self.ax_dist.set_ylim(0, 200)
        self.ax_dist.grid(True)
        self.line_dist, = self.ax_dist.plot([], [], 'b')

        self.ax_gyro = self.fig.add_subplot(313)
        self.ax_gyro.set_title("Giroscopio (rad/s)")
        self.ax_gyro.set_ylim(-5, 5)
        self.ax_gyro.grid(True)
        self.line_gx, = self.ax_gyro.plot([], [], 'r', label="GX")
        self.line_gy, = self.ax_gyro.plot([], [], 'g', label="GY")
        self.line_gz, = self.ax_gyro.plot([], [], 'b', label="GZ")
        self.ax_gyro.legend()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab_graf)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # -------- Loops --------
        self.leer_serial_1()
        self.leer_serial_2()
        self.actualizar_camara()

    # ---------- Serial ----------
    def abrir_serial(self, puerto):
        try:
            s = serial.Serial(puerto, BAUDIOS, timeout=0)
            time.sleep(2)
            print(f"Conectado a {puerto}")
            return s
        except:
            print(f"No se pudo abrir {puerto}")
            return None

    # ---------- PARSER CORREGIDO ----------
    def parsear_linea(self, linea):
        temp = None
        dist = None
        gyro = {}

        try:
            if "TEMP:" in linea:
                temp = float(linea.split("TEMP:")[1].split(",")[0])

            if "Distancia de objetos:" in linea:
                dist = float(linea.split("Distancia de objetos:")[1])

            for eje in ("GX", "GY", "GZ"):
                if eje + ":" in linea:
                    gyro[eje] = float(linea.split(eje + ":")[1].split(",")[0])
        except:
            pass

        return temp, dist, gyro

    # ---------- TEMP → ESCALA ----------
    def temp_a_escala(self, temp, t_min=15, t_max=40):
        temp = max(t_min, min(t_max, temp))
        return int(255 * (temp - t_min) / (t_max - t_min))

    # ---------- CÁMARA TÉRMICA ----------
    def actualizar_camara(self):
        if self.cap.isOpened() and self.temp_actual is not None:
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

    # ---------- PUERTO 1: TEMP + DIST ----------
    def leer_serial_1(self):
        if self.ser1 and self.ser1.in_waiting:
            try:
                linea = self.ser1.readline().decode("utf-8").strip()
                temp, dist, _ = self.parsear_linea(linea)

                if temp is not None:
                    #DATOS DE TEMPERATURA DEL SENSOR
                    self.temp_actual = temp
                    self.temp_data.append(temp)
                    self.lbl_temp.config(
                        text=f"Temperatura: {temp:.1f} °C"
                    )

                if dist is not None:
                    self.dist_data.append(dist)

                x = range(len(self.temp_data))
                self.line_temp.set_data(x, self.temp_data)
                self.line_dist.set_data(x, self.dist_data)

                self.ax_temp.set_xlim(0, MUESTRAS)
                self.ax_dist.set_xlim(0, MUESTRAS)

                self.canvas.draw_idle()
            except:
                pass

        self.root.after(200, self.leer_serial_1)

    # ---------- PUERTO 2: GIRO ----------
    def leer_serial_2(self):
        if self.ser2 and self.ser2.in_waiting:
            try:
                linea = self.ser2.readline().decode("utf-8").strip()
                _, _, g = self.parsear_linea(linea)

                if all(k in g for k in ("GX", "GY", "GZ")):
                    self.gx_data.append(g["GX"])
                    self.gy_data.append(g["GY"])
                    self.gz_data.append(g["GZ"])

                    x = range(len(self.gx_data))
                    self.line_gx.set_data(x, self.gx_data)
                    self.line_gy.set_data(x, self.gy_data)
                    self.line_gz.set_data(x, self.gz_data)

                    self.ax_gyro.set_xlim(0, MUESTRAS)
                    self.canvas.draw_idle()
            except:
                pass

        self.root.after(100, self.leer_serial_2)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()
