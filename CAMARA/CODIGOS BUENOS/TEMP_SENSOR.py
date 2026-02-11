import serial
import time
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import collections

# ---------------- CONFIG ----------------
PUERTO = "/dev/ttyUSB0"
BAUDIOS = 9600
MUESTRAS = 60

class MonitorDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor Ambiental")
        self.root.geometry("900x900")

        # Serial
        try:
            self.ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)
            time.sleep(2)
            print("Arduino conectado")
        except:
            self.ser = None
            print("No se pudo abrir el puerto")

        # Datos
        self.temp_data = collections.deque([0]*MUESTRAS, maxlen=MUESTRAS)
        self.dist_data = collections.deque([0]*MUESTRAS, maxlen=MUESTRAS)

        # Notebook
        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True)

        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Temperatura & Distancia")

        # Figura
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

        self.canvas = FigureCanvasTkAgg(self.fig, master=tab)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.actualizar()

    # ---------- PARSER ----------
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

    # ---------- LOOP ----------
    def actualizar(self):
        if self.ser and self.ser.in_waiting:
            try:
                linea = self.ser.readline().decode("utf-8").strip()
                temp, dist = self.parsear_linea(linea)

                if temp is not None:
                    self.temp_data.append(temp)

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

        self.root.after(300, self.actualizar)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorDashboard(root)
    root.mainloop()
