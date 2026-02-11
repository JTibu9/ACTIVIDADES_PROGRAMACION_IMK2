import serial
import time
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import collections

# ---------------- CONFIG ----------------
PUERTO_1 = "/dev/ttyUSB1"   # TEMP + DIST
PUERTO_2 = "/dev/ttyUSB0"   # GIROSCOPIO
BAUDIOS = 9600
MUESTRAS = 60

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard Multisensor")
        self.root.geometry("1000x700")

        # -------- Serial --------
        self.ser1 = self.abrir_serial(PUERTO_1)
        self.ser2 = self.abrir_serial(PUERTO_2)

        # -------- Buffers --------
        self.temp_data = collections.deque([0]*MUESTRAS, maxlen=MUESTRAS)
        self.dist_data = collections.deque([0]*MUESTRAS, maxlen=MUESTRAS)

        self.gx_data = collections.deque([0]*MUESTRAS, maxlen=MUESTRAS)
        self.gy_data = collections.deque([0]*MUESTRAS, maxlen=MUESTRAS)
        self.gz_data = collections.deque([0]*MUESTRAS, maxlen=MUESTRAS)

        # -------- Notebook --------
        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True)

        tab_graficas = ttk.Frame(notebook)
        notebook.add(tab_graficas, text="Gráficas")

        # -------- Figura --------
        self.fig = Figure(figsize=(9, 6), dpi=100)

        # TEMP
        self.ax_temp = self.fig.add_subplot(311)
        self.ax_temp.set_title("Temperatura (°C)")
        self.ax_temp.set_ylim(0, 50)
        self.ax_temp.grid(True)
        self.line_temp, = self.ax_temp.plot([], [], 'r', linewidth=2)

        # DIST
        self.ax_dist = self.fig.add_subplot(312)
        self.ax_dist.set_title("Distancia (cm)")
        self.ax_dist.set_ylim(0, 200)
        self.ax_dist.grid(True)
        self.line_dist, = self.ax_dist.plot([], [], 'b', linewidth=2)

        # GIRO
        self.ax_gyro = self.fig.add_subplot(313)
        self.ax_gyro.set_title("Giroscopio (rad/s)")
        self.ax_gyro.set_ylim(-5, 5)
        self.ax_gyro.grid(True)
        self.line_gx, = self.ax_gyro.plot([], [], 'r', label="GX")
        self.line_gy, = self.ax_gyro.plot([], [], 'g', label="GY")
        self.line_gz, = self.ax_gyro.plot([], [], 'b', label="GZ")
        self.ax_gyro.legend()

        self.canvas = FigureCanvasTkAgg(self.fig, master=tab_graficas)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # -------- Loops --------
        self.leer_serial_1()
        self.leer_serial_2()

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

    # ---------- Parser ----------
    def parsear(self, linea):
        datos = {}
        try:
            for bloque in linea.split(","):
                k, v = bloque.split(":")
                datos[k.strip()] = float(v)
        except:
            pass
        return datos

    # ---------- Puerto 1: TEMP + DIST ----------
    def leer_serial_1(self):
        if self.ser1 and self.ser1.in_waiting:
            linea = self.ser1.readline().decode().strip()
            d = self.parsear(linea)

            if "TEMP" in d:
                self.temp_data.append(d["TEMP"])
            if "DIST" in d:
                self.dist_data.append(d["DIST"])

            x = range(len(self.temp_data))
            self.line_temp.set_data(x, self.temp_data)
            self.ax_temp.set_xlim(0, MUESTRAS)

            self.line_dist.set_data(x, self.dist_data)
            self.ax_dist.set_xlim(0, MUESTRAS)

            self.canvas.draw_idle()

        self.root.after(200, self.leer_serial_1)

    # ---------- Puerto 2: GIRO ----------
    def leer_serial_2(self):
        if self.ser2 and self.ser2.in_waiting:
            linea = self.ser2.readline().decode().strip()
            d = self.parsear(linea)

            if all(k in d for k in ("GX", "GY", "GZ")):
                self.gx_data.append(d["GX"])
                self.gy_data.append(d["GY"])
                self.gz_data.append(d["GZ"])

                x = range(len(self.gx_data))
                self.line_gx.set_data(x, self.gx_data)
                self.line_gy.set_data(x, self.gy_data)
                self.line_gz.set_data(x, self.gz_data)
                self.ax_gyro.set_xlim(0, MUESTRAS)

                self.canvas.draw_idle()

        self.root.after(100, self.leer_serial_2)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()
