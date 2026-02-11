import cv2
import tkinter as tk
from PIL import Image, ImageTk

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Captura de video (0 = cámara por defecto)
        self.cap = cv2.VideoCapture(0)

        # Canvas donde se dibuja el video
        self.canvas = tk.Canvas(
            window,
            width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH),
            height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )
        self.canvas.pack()

        # Botón para salir
        self.btn_exit = tk.Button(window, text="Salir", command=self.close)
        self.btn_exit.pack(anchor=tk.CENTER, expand=True)

        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        ret, frame = self.cap.read()

        if ret:
            # OpenCV usa BGR, Tkinter necesita RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img = Image.fromarray(frame)
            self.photo = ImageTk.PhotoImage(image=img)

            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def close(self):
        self.cap.release()
        self.window.destroy()

# Ejecutar la app
App(tk.Tk(), "Tkinter + OpenCV")
